from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from fluent_pages.utils.polymorphicadmin import PolymorphicBaseModelAdmin, PolymorphicModelChoiceAdminForm
from fluent_pages.models import UrlNode
from mptt.admin import MPTTModelAdmin

class PageTypeChoiceAdminForm(PolymorphicModelChoiceAdminForm):
    def __init__(self, *args, **kwargs):
        super(PageTypeChoiceAdminForm, self).__init__(*args, **kwargs)
        self.fields['ct_id'].label = _("Page type")


def _get_polymorphic_type_choices():
    from fluent_pages.extensions import page_type_pool

    choices = []
    for plugin in page_type_pool.get_plugins():
        ct = ContentType.objects.get_for_model(plugin.model)
        choices.append((ct.id, plugin.verbose_name))

    choices.sort(key=lambda x: x[1])
    return choices


try:
    from django.contrib.admin import SimpleListFilter
except ImportError:
    extra_list_filters = ()
else:
    # Django 1.4:
    class PageTypeListFilter(SimpleListFilter):
        parameter_name = 'ct_id'
        title = _('page type')

        def lookups(self, request, model_admin):
            return _get_polymorphic_type_choices()

        def queryset(self, request, queryset):
            if self.value():
                queryset = queryset.filter(polymorphic_ctype_id=self.value())
            return queryset

    extra_list_filters = (PageTypeListFilter,)


class UrlNodePolymorphicAdmin(PolymorphicBaseModelAdmin, MPTTModelAdmin):
    """
    The main entry to the admin interface of django-fluent-pages.
    """
    base_model = UrlNode
    add_type_form = PageTypeChoiceAdminForm

    # Config list page:
    list_display = ('title', 'status_column', 'modification_date', 'actions_column')
    list_filter = ('status',) + extra_list_filters
    search_fields = ('slug', 'title')
    actions = ['make_published']
    change_list_template = None  # Restore Django's default search behavior, no admin/mptt_change_list.html


    class Media:
        css = {
            'screen': ('fluent_pages/admin.css',)
        }


    # ---- Polymorphic code ----

    def get_admin_for_model(self, model):
        from fluent_pages.extensions import page_type_pool
        return page_type_pool.get_model_admin(model)


    def get_polymorphic_model_classes(self):
        from fluent_pages.extensions import page_type_pool
        return page_type_pool.get_model_classes()


    def get_polymorphic_type_choices(self):
        """
        Return a list of polymorphic types which can be added.
        """
        return _get_polymorphic_type_choices()


    # ---- List code ----

    STATUS_ICONS = (
        (UrlNode.PUBLISHED, 'icon-yes.gif'),
        (UrlNode.DRAFT,     'icon-unknown.gif'),
    )


    def status_column(self, urlnode):
        status = urlnode.status
        title = [rec[1] for rec in UrlNode.STATUSES if rec[0] == status].pop()
        icon  = [rec[1] for rec in self.STATUS_ICONS if rec[0] == status].pop()
        if hasattr(settings, 'ADMIN_MEDIA_PREFIX'):
            admin = settings.ADMIN_MEDIA_PREFIX + 'img/admin/'  # Django 1.3
        elif getattr(settings, 'STATIC_URL', None):
            admin = settings.STATIC_URL + 'admin/img/'  # Django 1.4+
        return u'<img src="{admin}{icon}" width="10" height="10" alt="{title}" title="{title}" />'.format(admin=admin, icon=icon, title=title)

    status_column.allow_tags = True
    status_column.short_description = _('Status')


    def actions_column(self, urlnode):
        return u' '.join(self._actions_column_icons(urlnode))

    actions_column.allow_tags = True
    actions_column.short_description = _('actions')


    def _actions_column_icons(self, urlnode):
        empty_img = u'<span><img src="{static}fluent_pages/img/admin/blank.gif" width="16" height="16" alt=""/></span>'.format(static=settings.STATIC_URL)

        actions = []
        if urlnode.can_have_children:
            actions.append(
                u'<a href="add/?{parentattr}={id}" title="{title}"><img src="{static}fluent_pages/img/admin/page_new.gif" width="16" height="16" alt="{title}" /></a>'.format(
                    parentattr=self.model._mptt_meta.parent_attr, id=urlnode.pk, title=_('Add child'), static=settings.STATIC_URL)
                )
        else:
            actions.append(empty_img)

        if hasattr(urlnode, 'get_absolute_url') and urlnode.is_published:
            actions.append(
                u'<a href="{url}" title="{title}" target="_blank"><img src="{static}fluent_pages/img/admin/world.gif" width="16" height="16" alt="{title}" /></a>'.format(
                    url=urlnode.get_absolute_url(), title=_('View on site'), static=settings.STATIC_URL)
                )
        return actions


    def make_published(self, request, queryset):
        rows_updated = queryset.update(status=UrlNode.PUBLISHED)

        if rows_updated == 1:
            message = "1 page was marked as published."
        else:
            message = "{0} pages were marked as published.".format(rows_updated)
        self.message_user(request, message)


    make_published.short_description = _("Mark selected objects as published")
