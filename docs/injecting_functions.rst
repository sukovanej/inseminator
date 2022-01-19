Injecting functions
===================


It might be convinient to specify funcion's dependencies in-place. The great example is Flask
handler function. It should live in the same layer the DI container lives because it provides
only infrastructure functionality and desirably the only thing it does it calling domain layer's
functions. For this purpose, there is ``injector`` decorator on the ``Container`` object. You just
tell which dependency to provide using ``Depends`` type constructor::

   from inseminator import Container, Depends

   class Dependency:
      def __init__(self):
         self.x = 1

   container = Container()

   @container.inject
   def my_handler(input_value: int, dependency: Dependency = Depends(Dependency)):
      return input_value + dependency.x

Used like that, ``my_handler`` takes a single argument and thanks to closure it has ``dependency`` 
prepared with the right instance of ``Dependency``.


>>> my_handler(1)
2