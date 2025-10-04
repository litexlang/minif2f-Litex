# Reflections

## amc12a_2015_p10

litex能证明1,3,9,27,81是81的因子，但不能它们是唯一的因子（因为litex暂时没for i in range(1, 82) 的遍历去证明的办法）解决办法包括

1. 调用py库来计算81的因子，默认我们调用的库是对的（好处：这样做任何题目就会很容易，而且打印出来的时候很好看，如果让ai做题就会让ai有严格性：它是碉调包的，用完包然后把输出的结果贴在原地，非常准确），这样哪怕是自然语言编程也会很准确

2. 我内部引入对自然数上面的所有整数的遍历的证明，即引入for i in range(1, 82) 这样的遍历的办法

3. lean的写法是 example : 81.divisors = [1,3,9,27,81] := by decide 这里 by decide 是去计算 Nat.divisors 81 的值，Nat.divisors 81 的值是 [d for d in range(1..n) if d | n] 这样的。本质上它也是内置了for循环和know（即知道从1到81的整数，可以和range(1,82)一一对应

## mathd_algebra_13

这是很典型的 是且只是 的证明。可能用一个claim不太够