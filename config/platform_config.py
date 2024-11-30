class Config:
    def __init__(self, domain, title, price,previous_price, description):
        self.title = title
        self.domain = domain
        self.price = price
        self.previous_price = previous_price
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
        previous_price={
            "tag":"div",
            "attribute":"class",
            "attr_value":"yRaY8j A6+E6v"
            
        },
        description={
            "tag":"div",
            "attribute":"class",
            "attr_value":"yN+eNk"
            
        }
    ),
}
