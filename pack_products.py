from time import sleep
ROOK_POS = [0.5351460045577583, 0.06310454491140446, 0.12127944557182074]
BOTTLE_POS = [0.5415553600056415, 0.14232975533626466, 0.22013022259933934]
SPONGE_POS = [0.5563154741216328, 0.1871495748421237, 0.1278768754295184]
WITCHHAT_POS = [0.5271910841928377, -0.07120695997003954, 0.052176207437212185]
BOWL_POS = [0.5543423776840543, -0.12138974624720286, 0.01810995164858714]
D12_POS = [0.518854868200273, -0.0011941637511675499, 0.024168489690372386]
SHIPPING_POS = [0.05380281520840685, -0.31212749135838896, 0.42416930736250485]
def pack_products(product_list):
for product in product_list:
name = product[0].strip().lower()
if name == "rook":
position = ROOK_POS
elif name == "bottle":
position = BOTTLE_POS
elif name == "sponge":
position = SPONGE_POS
elif name == "witchhat":
position = WITCHHAT_POS
elif name == "bowl":
position = BOWL_POS
elif name == "d12":
position = D12_POS
else:
print("Error:", product[0], "is not a recognized product.")
continue
# Go to the item's location
arm.set_arm_position(position)
sleep(4)
# Hover over the shipping location
arm.set_arm_position(SHIPPING_POS)
sleep(4)
arm.home()

