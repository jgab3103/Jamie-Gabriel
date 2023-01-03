-- what is a type - collection of related values
-- e::t     e is an expression, will be evaluated as type t
-- every expression has a type
-- strongly typed, safter faster, no runtime type checks
-- :type not False
-- basic types
--  - bool
--  - char
--  - int
--  - string
--  - float
-- list of lists ok

['a', 'b', ['c', 'd']]    -- list of lists
(True, 'a', False) -- tupe of different lists, tuple is sequence 

('a', (False, 'c))

(True, ['a', 'b'])  -- type with bool and list, 

-- function is mapping of values of one type, to values of another type 

even(4) -- is even :: Int -> Bool

-- functions have 1 input type, 1 output type
-- add :: (Int, Int) -> Int

