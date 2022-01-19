Enforced parameters
===================

If it is not desired to provide a single concrete implementation for abstract or protocol dependency
one can enforce the resolver to use concrete types for specified parameters. Simply call ``container.resolve``
also with keywords and tell the resolve how it should resolve some particular parameters::

   container = Container()
   controller = container.resolve(Controller, domain_model=ConcreteDomainModel())

Moreover, using this approach ``ConcreteDomainModel`` is not evaluated and saved in the container but
rather in a sub-container which exists only during the resolving. Therefore, if we want to create
another instance that depends on ``DomainModel`` we must either use ``register`` or again specify
the parameter during resolving.