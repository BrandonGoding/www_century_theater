from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Movie


class MovieAdmin(ModelAdmin):
    model = Movie
    menu_label = "Movies"
    menu_icon = "media"
    menu_order = 1
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ["title", "open_date", "close_date", "review_page"]
    list_filter = ["open_date", "close_date"]
    search_fields = ["title", "open_date", "close_date", "imdb_id", "youtube_id"]


modeladmin_register(MovieAdmin)
