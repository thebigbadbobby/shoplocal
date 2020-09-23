## xpaths ##
store_input = {
        # "product_url": "https://shoplocalsantacruz.com/products/santa-cruz-sticker-variety",
        # "cart_url": "https://shoplocalsantacruz.com/checkout",
        # "card_name": "ShopLocal",
        # "fname": "Bobby",
        # "lname": "Missirian",
        # "email": "servicesflow@gmail.com",
        # "phone_number": "6789998212",
        # "street_address": "1179 Barbara Avenue",
        # "city": "Mountain View",
        # "zip_code": "94040",
        # "card_cvv": "823",
        # "region": "CA",
        # "card_number": "4400665047241177",
        # "card_expiry": "1023"

        "product_url": "https://shoplocalsantacruz.com/products/santa-cruz-sticker-variety",
        "cart_url": "https://shoplocalsantacruz.com/checkout",
        "card_name": 
        [
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')]",
                "//input[contains(@placeholder, 'CVV')]"
        ],
        "fname": 
        [
                '//input[@name="fname"]',
                "//input[contains(@name, 'name') and contains(@name, 'first')]"
        ],
        "lname": 
        [
                '//input[@name="lname"]',
                "//input[contains(@name, 'name') and contains(@name, 'last')]"
        ],
        "email": 
        [
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')]"
        ],
        "phone_number": 
        [
                "//*[contains(@data-test, 'phone')]",
                "//input[contains(@name, 'phone')]",
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]"
        ],
        "street_address": 
        [
                "//*[contains(@name, 'street')]",
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'address') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]"
        ],
        "city": 
        [
                "//*[contains(@name, 'city')]",
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'city')]"
        ],
        "zip_code": 
        [
                "//*[contains(@name, 'zip')]","//input[contains(@name, 'postal') and contains(@name, 'code')]","//input[contains(@placeholder, 'ZIP')]"
        ],
        "region": 
        [
                '//*[@name="state"]'
        ],
        "card_number": 
        [
                "//input[contains(@name, 'cardnumber')]",
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'number')]",
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card number')]"
        ],
        "card_expiry": 
        [
                "//input[contains(@name, 'exp')]",
                "//input[contains(@placeholder, 'MM') and contains(@placeholder, 'YY')]"
        ],
        "card_cvv": 
        [
                "//input[contains(@name, 'cvc')]",
                "//input[contains(@placeholder, 'CVV')]",
                "//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'security')]"
        ]
}
store_dropdown = {
        "//*[contains(@value, 'US')]": 
        [
                "//*[contains(@name, 'country')]"
        ],
        ".//*[contains(@value, 'CA')]":
        [
                "//*[contains(@name, 'region')]"
        ]
}
continue_buttons = [
        "//button//*[contains(text(), 'Next')/..]",
        "//button//*[contains(text(), 'Next')]/..",
        "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]",
        "//button//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]/.."
        ]

## stores##
stores = {
        "ShopLocal":
        {"https://shoplocalsantacruz.com/checkout": #shoplocal
                ["https://shoplocalsantacruz.com/products/santa-cruz-sticker-variety"]
        },
        "Artisans and Agency":
        {"https://www.artisanssantacruz.com/checkout": #shoplocal
                ["https://www.artisanssantacruz.com/collections/bath/products/rose-geranium-bar-soap-by-bonny-doon-farm"]
        },
        "Avatar Imports":
        {"https://avatarimports.net/checkout/": #shoplocal
                ["https://avatarimports.net/home-decor/single-size-batik-tapestry/"]
        },
        "Berdels":
        {"https://berdels.com/checkout/": #shoplocal
                ["https://berdels.com/products/rvca-sprout-claspback-hat-natural"]
        },
        "Bookshop Santa Cruz":
        {"https://www.botanicandluxe.com/store/checkout/#/payment": #shoplocal
                ["https://www.botanicandluxe.com/product/age-repair-hand-cream/2087"]
        },
        "Comicopolis":
        {"https://comicopolis.myshopify.com/checkout": #shoplocal
                ["https://comicopolis.myshopify.com/collections/games/products/blokus"]
        },
        "Far West Fungi":
        {"https://farwestfungi.com/checkout": #shoplocal
                ["https://farwestfungi.com/products/shiitake-jerky-pound?variant=15754356719714s"]
        },
        #### Farmer Freed website is wierd
        "Feejays":
        {"https://feejays.com/checkout": #shoplocal
                ["https://feejays.com/products/womens-classic-feejays?variant=12648324038769"]
        },
        "Fybr Bamboo":
        {"https://feejays.com/checkout": #shoplocal
                ["https://feejays.com/products/womens-classic-feejays?variant=12648324038769"]
        },
        


}

# "product_url": "https://shoplocalsantacruz.com/products/santa-cruz-sticker-variety",
default_shipping={
        "cart_url": "https://shoplocalsantacruz.com/checkout",
        "card_name": "ShopLocal",
        "fname": "Bobby",
        "lname": "Missirian",
        "email": "servicesflow@gmail.com",
        "phone_number": "6789998212",
        "street_address": "1179 Barbara Avenue",
        "city": "Mountain View",
        "zip_code": "94040",
        "card_cvv": "823",
        "region": "CA",
        "card_number": "5500666042071169",
        "card_expiry": "1023"
}
        