import json
import re

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from datasource import create_engine
from entity import *
from entry import Entry
from utils import contains

# Constants

REQUIRED_KEYS = [
    "latitude", "longitude", "date", "value"
]
SUB_ITEM_ENTRIES = {
    Entry("ocean", "OCEANS", "name", lambda x: Ocean(name=x), Ocean),
    Entry("region", "REGIONS", "name", lambda x: Region(name=x), Region),
    Entry("subregion", "SUBREGIONS", "name", lambda x: Subregion(name=x), Subregion),
    Entry("reference", "LONGREF", "title", lambda x: Reference(title=x), Reference),
    Entry("unit", "UNIT", "name", lambda x: Unit(name=x), Unit),
    Entry("sample_method", "SAMPMETHOD", "name", lambda x: SampleMethod(name=x), SampleMethod),
    Entry("organization", "ORG", "name", lambda x: Organization(name=x), Organization),
    Entry("doi", "DOI", "value", lambda x: DOI(value=x), DOI),
}

ON_CONFLICT_UPDATE_COLUMNS = [
    "ocean",
    "region",
    "subregion",
    "reference",
    "unit",
    "sample_method",
    "organization",
    "doi",
    "density_min",
    "density_max",
    "value",
    "global_id",
    "access_link",
]


# Function to extract unique values from a JSON file
def extract_unique_values(filepath):
    unique_values = {key: set() for key in SUB_ITEM_ENTRIES}
    with open(filepath) as file:
        data = json.load(file)["layers"][0]["features"]
        for feature in data:
            attr = feature["attributes"]
            for entry_type in SUB_ITEM_ENTRIES:
                if contains(attr, entry_type.entry_key):
                    unique_values[entry_type].add(attr[entry_type.entry_key])
    return unique_values


def upsert(engine, table_type: type, columns: [str], values, constraint_name):
    """
    Updates or inserts the items.
    :param engine: sqlalchemy engine instance
    :param table_type: entity class
    :param columns: target data columns
    :param values: mappings that consists each column in the columns params with values
    :param constraint_name: constraint that may incur constraint violation from given table
    """
    with Session(engine) as s:
        stmt = insert(table_type).values(values)
        set_stmt = {col: stmt.excluded[col] for col in columns}
        on_conflict_stmt = stmt.on_conflict_do_update(constraint=constraint_name, set_=set_stmt)
        s.execute(on_conflict_stmt)
        s.commit()
        s.flush()


def update_sub_items(filepath, engine):
    unique_values = extract_unique_values(filepath)
    for entry_type, values in unique_values.items():
        items = []
        col_name = entry_type.data_col_name
        for value in values:
            items.append({
                col_name: value
            })
        uq_name = "uq__{}__{}".format(entry_type.table_name, col_name)
        upsert(engine, entry_type.entity_class, [col_name], items, uq_name)


def parse_density_range(param) -> (float, float):
    s = re.sub(r"[^\d.-]*", "", param)
    items = s.split("-")
    if len(items) < 2:
        v = float(items[0])
        return v, v
    return float(items[0]), float(items[1])


def extract_measurement(feature):
    attr = feature["attributes"]
    m = {
        'latitude': feature["geometry"]["x"],
        'longitude': feature["geometry"]["y"],
        'global_id': attr["GlobalID"],
        'density_min': (parse_density_range(attr["DENSRANGE"]))[0],
        'density_max': (parse_density_range(attr["DENSRANGE"]))[1],
        'date': datetime.datetime.fromtimestamp(attr["Date"] / 1000),
        'access_link': attr["ACCESSLINK"],
        'value': attr["MEASUREMEN"]
    }
    for REQUIRED_KEY in REQUIRED_KEYS:
        if m[REQUIRED_KEY] is None:
            return None
    return m


# recall sub items with relevant ids
def recall_sub_items_entries(engine):
    results = {key.entry_key: {} for key in SUB_ITEM_ENTRIES}
    with Session(engine) as s:
        for entry in SUB_ITEM_ENTRIES:
            for row in s.query(entry.entity_class).all():
                results[entry.entry_key][row[entry.data_col_name]] = row.id
    return results


def insert_measurements(filepath, engine, sub_items, batch_count: int = 1000):
    items = []
    count = 0
    insert_count = 0
    try:
        with Session(engine) as session:
            with open(filepath) as file:
                data = json.load(file)["layers"][0]["features"]
                for feature in data:
                    attr = feature["attributes"]
                    m = extract_measurement(feature)
                    if m is None:
                        continue
                    for sub_item_type in SUB_ITEM_ENTRIES:
                        key = sub_item_type.entry_key
                        sub_items_by_type = sub_items[key]
                        sub_item_value = attr[key]
                        if contains(attr, key) and contains(sub_items_by_type, sub_item_value):
                            m[sub_item_type.table_name] = sub_items[key][attr[key]]
                        else:
                            m[sub_item_type.table_name] = None
                    items.append(m)
                    count += 1
                    if count == batch_count:
                        insert_count += __do_insert_measurements(session, items)
                        count = 0
                        items.clear()
        return insert_count + __do_insert_measurements(session, items)
    except Exception as e:
        print("error: {}".format(e))
    finally:
        if session:
            session.close()


def __do_insert_measurements(session, items) -> int:
    unique_items = {}
    size = 0

    for item in items:
        key = hash(str(item['latitude']) + str(item['longitude']) + str(item['date']))
        if key not in unique_items:
            size += 1
        unique_items[key] = item

    items.clear()
    cleaned_items = []

    for k, v in unique_items.items():
        cleaned_items.append(v)
    try:
        stmt = insert(Measurement).values(cleaned_items)
        on_conflict_stmt = stmt.on_conflict_do_update(
            constraint="uq__measurement__combined",
            set_={key: stmt.excluded[key] for key in ON_CONFLICT_UPDATE_COLUMNS},
        )
        session.execute(on_conflict_stmt)
        session.commit()
        return size
    except Exception as e:
        print("violation error occurred: {}".format(e))
        idx = 0
        for item in cleaned_items:
            print("item {}: {}".format(idx, item))
            idx += 1


def main():
    filepath = input("Please enter the target file path: ") or "Marine_Microplastics_WGS84_3566711509286026647.json"
    engine = create_engine()
    update_sub_items(filepath, engine)
    sub_items = recall_sub_items_entries(engine)
    inserted = insert_measurements(filepath, engine, sub_items)
    print("inserted {} measurements".format(inserted))


if __name__ == "__main__":
    main()
