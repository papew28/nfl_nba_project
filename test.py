import pandas as pd

data=pd.DataFrame({
    "date": ["Sun, Jan 01", "Mon, Jan 02", "Tue, Jan 03", "Wed, Jan 04", "Thu, Jan 05"]
})

# Définir le format de la chaîne de caractères
date_format = "%a, %b %d"

# Convertir la chaîne de caractères en datetime
datetime_object = pd.to_datetime(data["date"], format=date_format)
datetime_object=datetime_object.apply(lambda x: x.replace(year=2024).date())

print(datetime_object.to_list()[0])