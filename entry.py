class Entry:
    table_name: str
    entry_key: str
    data_col_name: str
    init_func: any
    entity_class: type

    def __init__(self, table_name: str, entry_key: str, data_col_name: str, init_func: any, entity_class: type):
        self.table_name = table_name
        self.entry_key = entry_key
        self.data_col_name = data_col_name
        self.init_func = init_func
        self.entity_class = entity_class

    def get_unique_constraint_name(self) -> str:
        return "uq__{}__{}".format(self.table_name, self.data_col_name)

    def to_entity(self, value):
        return self.init_func(value)
