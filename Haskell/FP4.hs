


-- list manipulation
head []
tail []
[1,2,3,4,5] !! 4 --select the nth element
take 3 [3,4,5] -- select first n elements
drop 3 [2,3,4,5]
length [3,4] -- length
sum [2,3,4]
product [3,4,5] -- note product [] is 1
[1,2,3] ++ [3,4,5] -- concatenate
reverse [3,4,5]
f a b + c*d -- lightweight function
f a + b -- is f(a) + b
last [4,5,6] -- get last
init [4,5,6] -- removes last element