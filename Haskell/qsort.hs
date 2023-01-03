main :: IO ()
main = return ()

qsort [] = []

qsort (x:xs) = qsort ys ++ [x] ++ qsort zs
 where
  ys = [a | a <- xs, a <= x]
  zs = [b | b <- xs, b > x]

--  sudo apt-get install haskell-platform -y