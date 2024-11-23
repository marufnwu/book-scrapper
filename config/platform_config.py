class Config:
    def __init__(self, title, price, description):
        self.title = title
        self.price = price
        self.description = description


PLATFORM_CONFIG = {
    "flipkart": Config(
        title={
            "tag":"span",
            "attribute":"class",
            "attr_value":"VU-ZEz"
            
        },
        price={
            "tag":"div",
            "attribute":"class",
            "attr_value":"Nx9bqj CxhGGd"
            
        },
        description={
            "tag":"div",
            "attribute":"class",
            "attr_value":"yN+eNk"
            
        }
    ),
}
