---
date: "2024-11-01T12:03:32+01:00"
draft: false
title: "JavaScript Filter Map Reduce"
---

These three functions are used to quickly manage data within lists. They are the JavaScript equivalent of LINQ.

## Filter

The **filter** function allows you to extract certain elements from the array based on a function.

```javascript
const numbers = [1, 4, 5, 6, 4, 2, 5, 6, 3, 1];
const even = numbers.filter((x) => x % 2 === 0);
console.log("Even numbers: ", even);
```

## Map

The **map** function allows you to apply a function to each element of the list.

```javascript
const numbers = [1, 4, 5, 6, 4, 2, 5, 6, 3, 1];
const squares = numbers.map((x) => x * x);
console.log("Squares: ", squares);
```

## Reduce

The **reduce** function performs a function on each element of the list and returns an "accumulated" result.

```javascript
const numbers = [1, 4, 5, 6, 4, 2, 5, 6, 3, 1];
const sum = numbers.reduce((accumulator, value) => {
  return accumulator + value;
}, 0);
console.log("Sum: ", sum);
```
