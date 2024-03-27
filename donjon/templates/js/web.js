"use strict"
let tab = ["quentin", "julien", 'charles', "nathan"]
let ch = "nathan"
let start = 3
let end = tab.length
let pas = 1

console.log("---------for classique----------")
for (let i = start; i < end; i += pas) {
    console.log(tab[i])
}

console.log("---------for in (renvoie contenu)----------")

for (let i in tab) {
    console.log(tab[i])
}

console.log("--------for in (renvoie indice)----------")

for (let i in ch) {
    console.log(i)
}

console.log("-------for of------------")

for (let elem of ch) {
    console.log(ch[elem])
}


console.log("-------boucle while------------")


let j = 0
while (j < 10) {
    console.log(j++)
}





let dic = {
    nathan: { class: '1TL1', age: 20 },
    C: { class: '1T', age: 22, tri: 'chais pas' }
}


console.log(`dic.C.age = ${dic.C.age}`)
console.log(`dic['C']['class'] = ${dic['C']['class']}`)


let tri = 'age'

console.log(`dic['C'][tri] = ${dic['C'][tri]}`)
console.log(`dic.C.tri = ${dic.C.tri}`)











