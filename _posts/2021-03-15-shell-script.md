---
title:  "shell script programming"
toc: true
toc_sticky: true
categories:
  - programming
tags:
  - shell
  - linux
---
# shell script practice
## 1. 스크립트 종료상태 확인하기
```bash
$ date
2021년 3월 15일 월요일 22시 14분 11초 KST
$ echo $?
0
$ dadaddasda
zsh: command not found: dadaddasda
$ echo $?
127
```
## 2. 리눅스 종료 상태 코드

|      코드      |      설명             |
| ------------- | -------------------  |
| 0             | 명령이 성공적으로 완료됨   |
| 1             | 일반 알 수 없는 오류     |
| 2             | 쉘 명령을 잘못 사용함    |
| 126           | 명령을 실행 할 수 없음    |
| 127             | 명령을 찾을 수 없음    |
| 128+x             | 치명적인 오류로 리눅스 신호 x를 포함    |
| 130           | \<ctrl\>+\<c\>로 명령이 종료됨   |