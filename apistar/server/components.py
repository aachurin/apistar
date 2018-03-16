import inspect


class Component():
    resolves_types = None

    def identity(self, parameter: inspect.Parameter):
        """
        Each component needs a unique identifier string that we use for lookups
        from the `state` dictionary when we run the dependency injection.
        """
        parameter_name = parameter.name.lower()
        annotation_name = parameter.annotation.__name__.lower()

        # If `resolve_parameter` includes `Parameter` then we use an identifier
        # that is additionally parameterized by the parameter name.
        args = inspect.signature(self.resolve).parameters.values()
        if inspect.Parameter in [arg.annotation for arg in args]:
            return annotation_name + ':' + parameter_name

        # Standard case is to use the class name, lowercased.
        return annotation_name

    def can_handle_parameter(self, parameter: inspect.Parameter):
        # Return `True` if this component can handle the given parameter.
        # The default behavior is for components to handle a particular
        # class or set of classes, however you could override this if you
        # wanted name-based parameter resolution.
        # Eg. Include the `Request` instance for any parameter named `request`.
        msg = 'Component %s must set "resolves_types" or override "can_handle_parameter"'
        assert self.resolves_types is not None, msg % self.__class__
        return parameter.annotation in self.resolves_types

    def resolve(self):
        raise NotImplementedError()
