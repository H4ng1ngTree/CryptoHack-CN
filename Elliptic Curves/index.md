---
layout: default
title: Elliptic Curves
---

# Elliptic Curves

## 原文简介

The use of elliptic curves for public-key cryptography was first suggested in 1985. After resisting decades of attacks, they started to see widespread use from around 2005, providing several benefits over previous public-key cryptosystems such as RSA.

Smaller EC keys offer greater strength, with a 256-bit EC key having the same security level as a 3072-bit RSA key. Furthermore, several operations using those keys (including signing) can be more efficient both time- and memory-wise. Finally, since ECC is more complex than RSA, it has the welcome effect of encouraging developers to make use of trusted libraries rather than rolling their own.

These challenges aim to give you an intuition for the trapdoor function behind ECC; dip your toes into the mathematical structure underlying it; and have you breaking popular schemes like ECDSA.

## 中文翻译

椭圆曲线在公钥密码中的应用最早于 1985 年被提出。经过几十年的攻击检验后，它们大约从 2005 年开始被广泛采用，并且相较于 RSA 之类的传统公钥系统，带来了不少优势。

更短的 EC 密钥就能提供更强的安全性：256 位椭圆曲线密钥大致相当于 3072 位 RSA 密钥的安全等级。同时，使用这些密钥的若干操作（包括签名）在时间和内存开销上也可能更高效。最后，由于 ECC 比 RSA 更复杂，它还有一个很实际的好处：会促使开发者优先使用可信库，而不是自己从头实现。

这一组题目会帮助你建立对 ECC 背后陷门函数的直觉，稍微摸到它的数学结构，并且让你有机会去破解一些常见方案，比如 ECDSA。

## 题目索引

- [Point Negation](./point-negation/)

