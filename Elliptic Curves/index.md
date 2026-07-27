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

椭圆曲线在公钥密码学中的应用最早于 1985 年被提出。经过数十年的攻击检验后，椭圆曲线密码学大约从 2005 年开始得到广泛使用，并且相较于 RSA 等早期公钥密码系统展现出若干优势。

更短的椭圆曲线密钥即可提供更高的安全强度。例如，256 位的椭圆曲线密钥大致可以达到 3072 位 RSA 密钥的安全等级。此外，基于这些密钥的一些操作，包括数字签名，在时间和内存开销上也可能更加高效。最后，由于 ECC 的实现复杂度高于 RSA，它也在客观上促使开发者更多地依赖经过验证的可信密码库，而不是自行实现底层算法。

本组挑战旨在帮助你建立对 ECC 背后陷门函数的直观理解，初步接触其底层数学结构，并进一步尝试分析和破解 ECDSA 等常见方案。

## 题目索引

- [Point Negation](./Point%20Negation/)
- [Point Addition](./Point%20Addition/)
