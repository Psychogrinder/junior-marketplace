from marketplace.marshmallow_schemas import OrderSchema, ConsumerSchema, ConsumerSignUpSchema, ProducerSchema, \
    ProducerSignUpSchema, CategorySchema, ProductSchema, CartSchema, CommentSchema

order_schema = OrderSchema()
consumer_schema = ConsumerSchema()
consumer_sign_up_schema = ConsumerSignUpSchema()
producer_schema = ProducerSchema()
producer_sign_up_schema = ProducerSignUpSchema()
category_schema = CategorySchema()
product_schema = ProductSchema()
cart_schema = CartSchema()
comment_schema = CommentSchema()
order_schema_list = OrderSchema(many=True)
consumer_schema_list = ConsumerSchema(many=True)
producer_schema_list = ProducerSchema(many=True)
category_schema_list = CategorySchema(many=True)
product_schema_list = ProductSchema(many=True)
comment_schema_list = CommentSchema(many=True)
