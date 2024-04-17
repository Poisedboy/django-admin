from geopy import geocoders
import requests
from django.conf import settings
from django.db.models.loading import get_model

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

from geopy import Point, Location, util


class GoogleGeocoder(geocoders.GoogleV3):

    def _parse_json(self, page, exactly_one=True):
        """Returns location, (latitude, longitude) from json feed."""
        places = page.get("results", [])
        if not len(places):
            self._check_status(page.get("status"))
            return None

        def parse_place(place):
            """Get the location, lat, lng from a single json place."""
            location = place.get("formatted_address")
            country = None
            country_short = None
            city = None
            for comp in place["address_components"]:
                # Hardcoding tokio because of https://groups.google.com/forum/#!topic/google-places-api/vaWdixpouRQ
                if "country" in comp["types"]:
                    country = comp["long_name"]
                    country_short = comp["short_name"]
                if "locality" in comp["types"] or comp["long_name"] in ["Tokyo"]:
                    city = comp["long_name"]
                if country in ["Singapore", "Monaco", "Vatican City", "Hong Kong"]:
                    city = country
            latitude = place["geometry"]["location"]["lat"]
            longitude = place["geometry"]["location"]["lng"]
            return {
                "location": location,
                "city": city,
                "country": country,
                "country_short": country_short,
                "latitude": latitude,
                "longitude": longitude,
            }

        if exactly_one:
            return parse_place(places[0])
        else:
            return [parse_place(place) for place in places]


class GoogleGeocoderDirect:

    def getData(self, data):
        if data in ["Singapore", "Monaco", "Vatican City", "Hong Kong"]:
            pass
        else:
            location_parts = data.split(",")
            city_sent = location_parts[0].strip()
            country_sent = location_parts[-1].strip()
            if country_sent == "Australia":
                city_got = (
                    get_model("lbb", "City")
                    .objects.filter(
                        title=city_sent, country__title=country_sent, active=True
                    )
                    .first()
                )

                if city_got:
                    pass
                else:
                    city_part_sent = location_parts[0].strip().split(" ")
                    if len(city_part_sent) > 1:
                        city_sent = " "
                        city_sent = city_sent.join(city_part_sent[:-1])
                    else:
                        city_sent = location_parts[0].strip()

                    city_got = (
                        get_model("lbb", "City")
                        .objects.filter(
                            title__icontains=city_sent,
                            country__title=country_sent,
                            active=True,
                        )
                        .first()
                    )
                    if city_got:
                        pass
                    else:
                        city_got = (
                            get_model("lbb", "City")
                            .objects.filter(
                                title__icontains=city_sent, country__title=country_sent
                            )
                            .first()
                        )
            else:
                city_got = (
                    get_model("lbb", "City")
                    .objects.filter(title=city_sent, country__title=country_sent)
                    .first()
                )
            if city_got:
                location = city_got.country.location
                country = city_got.country.title
                country_short = city_got.country.location
                city = city_got.title
                return {
                    "location": location,
                    "city": city,
                    "country": country,
                    "country_short": country_short,
                }

        final = data.replace(" ", "+")
        final = final.replace(",+", ",")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (
            final,
            getattr(settings, "EASY_MAPS_GOOGLE_KEY"),
        )
        response = requests.post(url, timeout=300)
        if response:
            jsonif = response.json()
            if len(jsonif["results"]):
                place = jsonif["results"][0]
                location = place["formatted_address"]
                country = None
                country_short = None
                city = None
                check = {}
                check["locality"] = None
                check["postal_town"] = None
                check["sublocality_level_1"] = None
                check["administrative_area_level_3"] = None
                for comp in place["address_components"]:
                    # Hardcoding tokio because of https://groups.google.com/forum/#!topic/google-places-api/vaWdixpouRQ
                    if "country" in comp["types"]:
                        country = comp["long_name"]
                        country_short = comp["short_name"]
                    if "locality" in comp["types"] or comp["long_name"] in [
                        "Tokyo",
                        "Washington",
                        "Jakarta",
                        "Seoul",
                    ]:
                        check["locality"] = comp
                    if "postal_town" in comp["types"]:
                        check["postal_town"] = comp
                    if "sublocality_level_1" in comp["types"]:
                        check["sublocality_level_1"] = comp
                    if "administrative_area_level_3" in comp["types"]:
                        check["administrative_area_level_3"] = comp

                if country in ["Singapore", "Monaco", "Vatican City", "Hong Kong"]:
                    city = country
                elif check["locality"]:
                    city = check["locality"]["long_name"]
                elif check["postal_town"]:
                    city = check["postal_town"]["long_name"]
                elif check["sublocality_level_1"]:
                    city = check["sublocality_level_1"]["long_name"]
                elif check["administrative_area_level_3"]:
                    city = check["administrative_area_level_3"]["long_name"]

                latitude = place["geometry"]["location"]["lat"]
                longitude = place["geometry"]["location"]["lng"]
                return {
                    "location": location,
                    "city": city,
                    "country": country,
                    "country_short": country_short,
                    "latitude": latitude,
                    "longitude": longitude,
                }
            else:
                return None
        else:
            return None
