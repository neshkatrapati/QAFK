VIEWS = {}
def view(app, name):
    def _view(method):
        VIEWS[app + "." + name] = method
        def _view_method(container, args=None):
            return method(container, args)
        return _view_method
    return _view
