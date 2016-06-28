# CubesViewer
#
# Copyright (c) 2012-2014 Jose Juan Montes, see AUTHORS for more details
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# If your version of the Software supports interaction with it remotely through
# a computer network, the above copyright notice and this permission notice
# shall be accessible to all users.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from django.views.generic.base import TemplateView
from django.conf import settings
from get_engagements import *

class CubesViewerView(TemplateView):

    template_name = "cubesviewer/index.html"
    exclude = ()

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context["cubesviewer_cubes_url"] = settings.CUBESVIEWER_CUBES_URL
        context["cubesviewer_backend_url"] = settings.CUBESVIEWER_BACKEND_URL
	context["showAllSaved"] = 0
        return context


class CubesViewerSavedView(TemplateView):
    template_name = "cubesviewer/index.html"
    exclude = ()

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context["cubesviewer_cubes_url"] = settings.CUBESVIEWER_CUBES_URL
        context["cubesviewer_backend_url"] = settings.CUBESVIEWER_BACKEND_URL
	context["showAllSaved"] = 1
        return context

def get_post_engagements(request):
	return get_post_by_engagements()

def get_post_shares(request):
	return get_post_by_shares()

def get_post_unique_users(request):
	return get_post_by_unique_users()

def get_comments_authors(request):
	return get_comments_by_authors()

def get_engagements_authors(request):
	return get_engagements_by_authors()
