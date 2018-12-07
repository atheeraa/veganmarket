from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Department, Base, Item

engine = create_engine('sqlite:///veganmarket.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#bakery
department1 = Department(name="Bakery", image="/static/bakery.jpg")

session.add(department1)
session.commit()

item1 = Item(name="Organic Banana Cake ", description="A vegan cake made with organic bananas and apple juice.",
                     price="$3.50" , department=department1 )

session.add(item1)
session.commit()

item2 = Item(name="Cookie Coconut Chocolate Chip  ", description="Find the perfect combination of fresh shredded coconut and scrumptious chocolate in this protein rich",
                     price="$2.90", department=department1)

session.add(item2)
session.commit()

item2 = Item(name="Vanilla Wafers  ", description="Gluten-free.Perfect for kids! Light and crispy.Free from wheat, milk and egg.",
                     price="$2.90", department=department1)

session.add(item2)
session.commit()

item3 = Item(name="Everfresh Organic Malted Raisin Loaf ", description="A vegan cake made with wholemeal wheat and malted barley flours, organic raisins and dark molasses.",
                     price="$1.94", department=department1)

session.add(item2)
session.commit()


#jams and spread
department2 = Department(name="Jams and spreads", image="/static/jams.jpg")

session.add(department2)
session.commit()

item1 = Item(name="Organic Dark Chocolate & Hazelnut Spread " , description="Mr Organic's Dark Chocolate & Hazelnut Spread promises a deeper flavour and a genuine  ",
                     price="$3.99", department=department2)

session.add(item1)
session.commit()


item2 = Item(name="Organic Raspberry Jam" , description="Bionova jams are made from the finest fruits from organic harvest. The sugar is imported from brazil and is fairtrade. This fruit jam is made by hand using the highest quality organic fruits. ",
                     price="$2.55", department=department2)

session.add(item2)
session.commit()


item3 = Item(name="Dark Chocolate Spread" , description="This is another fantasticly made organic dark chocolate spread packed with taste and made with extra special care. Made with low fat coco powder and soya flour to add healthy alternatives and still maintain great taste!This is another fantasticly made org",                     price="$3.59", department=department2)

session.add(item3)
session.commit()

 
    



department3 = Department(name="Cheese", image="/static/cheese.jpg")

session.add(department3)
session.commit()



item1 = Item(name="Schlagfix Spread Vegan Mascarpone" , description="Unique, delicious and sustainable. This is the new Mascarpone plant cream from Schlagfix.",
                     price="$3.49", department=department3)

session.add(item1)
session.commit()

item2 = Item(name="Ricotta" , description="Plant-based alternative to ricotta, natural.",
                     price="$6.65", department=department3)

session.add(item2)
session.commit()

item3 = Item(name="Smoked Gouda Slices" , description="Soya-Free Smoked Gouda Style Slices, Elevate your cheese party with this decadent hickory-smoked Gouda",
                     price="$3.39", department=department3)

session.add(item3)
session.commit()


department4 = Department(name="Coffee", image="/static/coffee.jpg")

session.add(department4)
session.commit()

item1 = Item(name="Classic Cappuccino Mix " , description=" A cappuccino mix thats not only vegan but also tastes great. Creamy, rich and instant - just add hot water ",
                     price="$5.49", department=department4)

session.add(item1)
session.commit()


item2 = Item(name="Guatemalan Coffee Beans" , description=" Organic whole coffee beans from Equal Exchange, sourced from small farmer co-operatives in remote regions of south western Guatemala. ",
                   price="$4.89", department=department4)

session.add(item2)
session.commit()

print "added menu items!"
