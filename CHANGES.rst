Changelog
=========

Changes in git
--------------

* Added ``draft`` CSS class to unpublished menu items that are only visible for staff members.
* Added ``FluentPagesConfig`` to use Django 1.7 appconfigs.
* Added multiple fallback language support for django-parler_ 1.5.
* Improve error messages when URLs can't be created.
* Improve performance of ``PageSitemap`` for sites with a lot of pages.
* Temporary fix: Block moving pages to untranslated sub nodes, until a design decision can be made how to handle this.
* Temporary fix: Hide subpages when searching in the admin, to avoid errors with partial MPTT trees.
* Fixed Django 1.8 issues in the "Change Page" view.
* Fixed silent behavior of using ``.parent_site()`` too late in an already filtered queryset.
* Fixed unicode handling in ``rebuild_page_tree``.


Changes in version 0.9
----------------------

* Added Django 1.8 support
* Non-published pages can now be seen by staff members
* Fix initial migrations on MySQL with InnoDB/utf8 charset.
* Fix missing ``robots.txt`` in the PyPI package.
* Fix behavior of ``Page.objects.language(..).get_for_path()`` and ``best_match_for_path()``, use the currently selected language.
  This is similar to django-parler_'s ``TranslatableModel.objects.language(..).create(..)`` support.
* Fix skipping mount-points in ``app_reverse()`` when the root is not translated.
* *Backwards incompatible* with previous beta releases: split the ``fluent_pages.integration.fluent_contents`` package.
  You'll need to import from the ``.models.``, ``.admin`` and ``.page_type_plugins`` explicitly.
  This removes many cases where projects suffered from circular import errors.


Released in 0.9c1:
~~~~~~~~~~~~~~~~~~

* Fix deleting pages which have SEO fields filled in (the ``HtmlPageTranslation`` model).
* Fix ``UrlNode.DoesNotExist`` exception when using ``{% render_breadcrumb %}`` on 404 pages.
* Change ``slug`` size to 100 characters.
* Added ``RobotsTxtView`` for easier sitemaps integration
* Added ``FluentContentsPage.create_placeholder(slot)`` API.
* Added ``--mptt-only`` option to ``manage.py rebuild_page_tree`` command.
* Added lazy-resolver functions: ``app_reverse_lazy()`` / ``mixed_reverse_lazy()``.


Released in 0.9b4:
~~~~~~~~~~~~~~~~~~

* Fix South migrations for flexible ``AUTH_USER_MODEL``


Released in 0.9b3:
~~~~~~~~~~~~~~~~~~

* Added preliminary Django 1.7 support, migrations are not fully working yet.
* Added translation support for the SEO fields (meta keywords/description/title) and redirect URL.
* All base models are proxy models now; there will be no more need to update south migrations in your own apps.
* Added ``fluent_pages.integration.fluent_contents`` to simplify creating custom
* Added ``CurrentPageMixin`` and ``CurrentPageTemplateMixin`` for custom views.
* Added ``HtmPage.meta_robots`` property to automatically add ``noindex`` to pages outside the sitemaps.
* Added ``in_sitemaps`` flag, which is now false for the ``RedirectNode`` by default.
  pagetypes that reuse the django-fluent-contents_ integration that the ``fluent_pages.pagetypes.fluentpage`` has.
* Fixed stale translated ``ContentItem`` objects from django-fluent-contents_ when deleting a translation of a page.
* Fixed support for: future >= 0.13.
* Fixed support for: django-polymorphic >= 0.6.
* Fixed support for: django-parler >= 1.2.
* API: use ``FluentContentsPage`` instead of ``AbstractFluentPage``.


Upgrade notices:
~~~~~~~~~~~~~~~~

Due to Django 1.7 support, the following changes had to be made:

* ``fluent_pages.admin`` is renamed to ``fluent_pages.adminui``.
* South 1.0 is now required to run the migrations (or set ``SOUTH_MIGRATION_MODULES`` for all plugins).

Secondly, there were database changes to making the SEO-fields translatable.
Previously, the SEO fields were provided by abstract models, requiring projects to upgrade their apps too.

All translated SEO fields are now managed in a single table, which is under the control of this app.
Fortunately, this solves any future migration issues for changes in the ``HtmlPage`` model.

If your page types inherited from ``HtmlPage``, ``FluentContentsPage`` or it's old name ``FluentPage``,
you'll have to migrate the data of your apps one more time.
The bundled pagetypes have two migrations for this: ``move_seo_fields`` and ``remove_untranslatad_fields``.
The first migration moves all data to the ``HtmlPageTranslation`` table (manually added to the datamigration).
The second migration can simply by generated with ``./manage.py schemamigration <yourapp> --auto "remove_untranslatad_fields"``.

If you have overridden ``save_translation()`` in your models, make sure to check for ``translation.related_name``,
as both the base object and derived object translations are passed through this method now.

The ``SeoPageMixin`` from 0.9b1 was removed too, instead inherit directly from ``HtmlPage``.


Released in 0.9b2:
~~~~~~~~~~~~~~~~~~

* Added Python 3 support!
* Added ``key`` field to allow linking to specific user-created pages (e.g. a Terms and Conditions page).
  This feature is only visible when ``FLUENT_PAGES_KEY_CHOICES`` is configured.
* Fix support for ``i18n_patterns()`` in the ``override_url`` field.
* Added ``hide_untranslated_menu_items`` setting in ``FLUENT_PAGES_LANGUAGES`` / ``PARLER_LANGUAGES``.
* Added ``page`` variable for menu items in ``PageNavigationNode``.
* Add "change Override URL permission" flag.
  South users: run ``manage.py syncdb --all`` to create the permission
* Fix resolving pages under their fallback language URL when a translated URL does exist.
* Fix exception in ``PageNavigationNode.has_children``.
* Fix moving pages in the admin list (changes were undone).
* Fix missing "ct_id" GET parmeter for Django 1.6 when filtering in the admin (due to the ``_changelist_filters`` parameter).
* Updated dependencies to their Python 3 compatible versions.
* Optimize queries for rendering menu's

 * nodes without children no need a query in ``PageNavigationNode.children``.
 * avoid polymorphic behavior for child menu nodes (unless the parent node was polymorphic).


Released in 0.9b1:
~~~~~~~~~~~~~~~~~~

* Added multisite support.
* Added multilingual support, using django-parler_.
* Added hooks for patching the admin; ``FLUENT_PAGES_PARENT_ADMIN_MIXIN`` and ``FLUENT_PAGES_CHILD_ADMIN_MIXIN``.
  Note that using this feature is comparable to monkey-patching, and future compatibility can't be fully guanteed.
* Added "Can change Shared fields" permission for all page types.
* Added "Can change Page layout" permission for ``fluent_pages.pagetypes.fluentpage``.
* Allow ``formfield_overrides`` to contain field names too.
* API: added ``SeoPageMixin`` model with ``meta_title``, ``meta_keywords`` and ``meta_description`` fields.
* API: renamed ``FluentPageBase`` to ``AbstractFluentPage``.
* API: added ``get_view_response`` to the ``PageTypePlugin`` class, allow adding middleware to custom views.
* API: **Backwards incompatible:** when inheriting from the abstract ``HtmlPage`` model, your app needs a South migration.
* Fixed calling ``reverse()`` on the resolved page urls.
* Dropped Django 1.3 and 1.4 support.


Upgrade notices:
~~~~~~~~~~~~~~~~

* When using custom page types that inherit from inherited from ``HtmlPage``, ``FluentPageBase`` or ``FluentContentsPage``,
  please add a South migration to your application to handle the updated fields.

 * The ``keywords`` field was renamed to ``meta_keywords``.
 * The ``description`` field was renamed to ``meta_description``.
 * The ``meta_title`` field was added.
 * The South ``rename_column`` function can be used in the migration::

     db.rename_column('your_model_table', 'keywords', 'meta_keywords')
     db.rename_column('your_model_table', 'description', 'meta_description')

* API: renamed ``FluentPageBase`` to ``FluentContentsPage``.
  The old name is still available.


Changes in version 0.8.7
------------------------

* Add support of django-polymorphic 0.6.
* Add ``page`` variable for menu items in ``PageNavigationNode``.


Changes in version 0.8.6
------------------------

* Add ``FLUENT_PAGES_DEFAULT_IN_NAVIGATION`` setting to change the "in navigation" default value.
* Fix django-mptt_ 0.6 support.
* Fix using `{% appurl %}` for modules with multiple results.
* Widen "modification date" column, to support other languages.


Changes in version 0.8.5
------------------------

* Added intro page for empty sites.
* Support Django 1.6 transaction management.
* Fix NL translation of "Slug".
* Fix the @admin redirect for application URLs (e.g. ``/page/app-url/@admin`` should redirect to ``/page/app-url/``).
* Fix URL dispatcher for app urls when a URL prefix is used (e.g. ``/en/..``)
* Fix Django 1.5 custom user model support in migrations


Changes in version 0.8.4
------------------------

* Fix running at Django 1.6 alpha 1
* Remove filtering pages by SITE_ID in ``PageChoiceField`` as there is no proper multi-site support yet.
* Remove ``X-Object-Type`` and ``X-Object-Id`` headers as Django 1.6 removed it due to caching issues.


Changes in version 0.8.3
------------------------

* Fix circular imports for some setups that import ``fluent_pages.urlresolvers`` early.
* Fix initial south migrations, added missing dependencies.
* Fix using ``{% render_menu %}`` at 404 pages.


Changes in version 0.8.2
------------------------

* Add ``parent`` argument to ``{% render_menu %}``, to render sub menu's.
* Add ``page``, ``site`` variable in template of ``{% render_breadcrumb %}``.
* Add ``request``, ``parent`` (the parent context) variables to templates of ``{% render_breadcrumb %}`` and ``{% render_menu %}``.
* Bump version requirement of django-mptt_ to 0.5.4, earlier versions have bugs.
* Fix ``{% get_fluent_page_vars %}`` to skip the django-haystack_ ``page`` variable.
* Fix ``{% get_fluent_page_vars %}`` when a ``site`` variable is already present.
* Fix unit test suite in Django 1.3


Changes in version 0.8.1
------------------------

* Add "Flat page" page type.
* Add support for django-any-urlfield_.
* Add ``X-Object-Type`` and ``X-Object-Id`` headers to the response in development mode (similar to django.contrib.flatpages_).
* Add Django 1.5 Custom User model support.
* Added lots of documentation.
* Moved the template tag parsing to a separate package, django-tag-parser_.
* Improve error messages on initial project setup.
* Improve ability to extend the page change_form template.
* Improve layout of *keywords* and *description* fields in the admin.
* Fixed 500 error on invalid URLs with unicode characters.
* Fixed ``app_reverse()`` function for Django 1.3.
* Fixed ``appurl`` tag for template contexts without *page* variable.
* Fixed ``NavigationNode.is_active`` property for sub menu nodes.
* Fixed ``NavigationNode.parent`` property for root node.
* Fixed ``runtests.py`` script.
* Fixed ``Page.objects.best_match_for_path()`` for pages without a slash.
* Fixed generated URL path for "file" node types in sub folders.
* Fix Django dependency in ``setup.py``, moved from ``install_requires`` to the ``requires`` section.
* Bump version of django-polymorphic-tree_ to 0.8.6 because it fixes issues with moving pages in the admin.


Version 0.8.0
-------------

First public release

* Support for custom page types.
* Optional integration with django-fluent-contents_.
* Refactored tree logic to django-polymorphic-tree_.
* Unit tests included.

.. _django-any-urlfield: https://github.com/edoburu/django-any-urlfield
.. _django.contrib.flatpages: https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/
.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _django-haystack: http://haystacksearch.org/
.. _django-mptt: https://github.com/django-mptt/django-mptt
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-polymorphic-tree: https://github.com/edoburu/django-polymorphic-tree
.. _django-tag-parser: https://github.com/edoburu/django-tag-parser
