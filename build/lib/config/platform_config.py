class Config:
    def __init__(self, domain, title, price, description):
        self.title = title
        self.domain = domain
        self.price = price
        self.description = description


PLATFORM_CONFIG = {
    "flipkart": Config(
        domain="https://flipkart.com",
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
