// ==================== НАИВНЫЙ ПАРСЕР ====================
function naiveParseS(str) {
    let results = [];
    
    // Правило 3: S → a a
    if (str === 'aa') {
        results.push({x: 1});
    }
    
    // Правило 1: S → a S S a
    if (str.length >= 4 && str[0] === 'a' && str[str.length - 1] === 'a') {
        const middle = str.slice(1, -1);
        for (let splitPos = 1; splitPos < middle.length; splitPos++) {
            const leftPart = middle.slice(0, splitPos);
            const rightPart = middle.slice(splitPos);
            
            const leftResults = naiveParseS(leftPart);
            const rightResults = naiveParseS(rightPart);
            
            for (const leftRes of leftResults) {
                for (const rightRes of rightResults) {
                    if (leftRes.x === rightRes.x) {
                        results.push({x: leftRes.x + rightRes.x + 2});
                    }
                }
            }
        }
    }
    
    // Правило 2: S → S S b S S
    if (str.length >= 5) {
        for (let bPos = 0; bPos < str.length; bPos++) {
            if (str[bPos] === 'b') {
                if (bPos >= 2 && bPos <= str.length - 3) {
                    const beforeB = str.slice(0, bPos);
                    for (let split1 = 1; split1 < beforeB.length; split1++) {
                        const s1 = beforeB.slice(0, split1);
                        const s2 = beforeB.slice(split1);
                        
                        const afterB = str.slice(bPos + 1);
                        for (let split2 = 1; split2 < afterB.length; split2++) {
                            const s3 = afterB.slice(0, split2);
                            const s4 = afterB.slice(split2);
                            
                            const s1Results = naiveParseS(s1);
                            const s2Results = naiveParseS(s2);
                            const s3Results = naiveParseS(s3);
                            const s4Results = naiveParseS(s4);
                            
                            for (const r1 of s1Results) {
                                for (const r2 of s2Results) {
                                    for (const r3 of s3Results) {
                                        for (const r4 of s4Results) {
                                            if (r2.x === r4.x) {
                                                results.push({x: r1.x + r3.x});
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    // Правило 4: S → b S b
    if (str.length >= 3 && str[0] === 'b' && str[str.length - 1] === 'b') {
        const middle = str.slice(1, -1);
        const middleResults = naiveParseS(middle);
        
        for (const middleRes of middleResults) {
            results.push({x: middleRes.x});
        }
    }
    
    return results;
}

function naiveParse(str) {
    const results = naiveParseS(str);
    return {
        success: results.length > 0,
        x: results.length > 0 ? results[0].x : null
    };
}
// ==================== ОПТИМИЗИРОВАННЫЙ ПАРСЕР ====================
function optimizedParseS(str, memo = new Map()) {
    if (memo.has(str)) return memo.get(str);
    
    let results = [];
    
    // Быстрые проверки для отсечения невозможных случаев
    // 1. Длина должна быть >= 2 (минимальное правило S → aa)
    if (str.length < 2) {
        memo.set(str, results);
        return results;
    }
    
    // 2. Проверка на наличие подстроки 'aa'
    if (!str.includes('aa')) {
        memo.set(str, results);
        return results;
    }
    
    // 3. Число букв 'a' должно быть четным
    const aCount = (str.match(/a/g) || []).length;
    if (aCount % 2 !== 0) {
        memo.set(str, results);
        return results;
    }
    
    // Правило 3: S → a a
    if (str === 'aa') {
        results.push({x: 1});
    }
    
    // Правило 1: S → a S S a
    if (str.length >= 4 && str[0] === 'a' && str[str.length - 1] === 'a') {
        const middle = str.slice(1, -1);
        // Оптимизация: перебираем только такие разбиения, где обе части содержат 'aa'
        for (let splitPos = 1; splitPos < middle.length; splitPos++) {
            const leftPart = middle.slice(0, splitPos);
            const rightPart = middle.slice(splitPos);
            
            // Быстрая проверка: обе части должны содержать 'aa'
            if (!leftPart.includes('aa') || !rightPart.includes('aa')) continue;
            
            const leftResults = optimizedParseS(leftPart, memo);
            const rightResults = optimizedParseS(rightPart, memo);
            
            for (const leftRes of leftResults) {
                for (const rightRes of rightResults) {
                    if (leftRes.x === rightRes.x) {
                        results.push({x: leftRes.x + rightRes.x + 2});
                    }
                }
            }
        }
    }
    
    // Правило 2: S → S S b S S
    if (str.length >= 5) {
        // Ищем только такие 'b', где части содержат 'aa'
        for (let bPos = 0; bPos < str.length; bPos++) {
            if (str[bPos] === 'b') {
                if (bPos >= 2 && bPos <= str.length - 3) {
                    const beforeB = str.slice(0, bPos);
                    const afterB = str.slice(bPos + 1);
                    
                    // Быстрая проверка: обе части должны содержать 'aa'
                    if (!beforeB.includes('aa') || !afterB.includes('aa')) continue;
                    
                    for (let split1 = 1; split1 < beforeB.length; split1++) {
                        const s1 = beforeB.slice(0, split1);
                        const s2 = beforeB.slice(split1);
                        
                        // Быстрая проверка: s1 и s2 должны содержать 'aa'
                        if (!s1.includes('aa') || !s2.includes('aa')) continue;
                        
                        for (let split2 = 1; split2 < afterB.length; split2++) {
                            const s3 = afterB.slice(0, split2);
                            const s4 = afterB.slice(split2);
                            
                            // Быстрая проверка: s3 и s4 должны содержать 'aa'
                            if (!s3.includes('aa') || !s4.includes('aa')) continue;
                            
                            const s1Results = optimizedParseS(s1, memo);
                            const s2Results = optimizedParseS(s2, memo);
                            const s3Results = optimizedParseS(s3, memo);
                            const s4Results = optimizedParseS(s4, memo);
                            
                            for (const r1 of s1Results) {
                                for (const r2 of s2Results) {
                                    for (const r3 of s3Results) {
                                        for (const r4 of s4Results) {
                                            if (r2.x === r4.x) {
                                                results.push({x: r1.x + r3.x});
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    // Правило 4: S → b S b
    if (str.length >= 3 && str[0] === 'b' && str[str.length - 1] === 'b') {
        const middle = str.slice(1, -1);
        // Быстрая проверка: middle должна содержать 'aa'
        if (middle.includes('aa')) {
            const middleResults = optimizedParseS(middle, memo);
            for (const middleRes of middleResults) {
                results.push({x: middleRes.x});
            }
        }
    }
    
    // Убираем дубликаты (одинаковые значения x)
    const uniqueResults = [];
    const seen = new Set();
    for (const res of results) {
        if (!seen.has(res.x)) {
            seen.add(res.x);
            uniqueResults.push(res);
        }
    }
    
    memo.set(str, uniqueResults);
    return uniqueResults;
}

function optimizedParse(str) {
    const results = optimizedParseS(str);
    return {
        success: results.length > 0,
        x: results.length > 0 ? results[0].x : null,
        memoSize: optimizedParseS.memo ? optimizedParseS.memo.size : 0
    };
}

function generateRandomString(length) {
    const alphabet = ['a', 'b'];
    let result = '';
    for (let i = 0; i < length; i++) {
        result += alphabet[Math.floor(Math.random() * alphabet.length)];
    }
    return result;
}

function testBothParsers(str) {
    console.log(`\nТестируем строку: "${str}"`);
    
    const start1 = performance.now();
    const naiveResult = naiveParse(str);
    const time1 = performance.now() - start1;
    
    const start2 = performance.now();
    const optimizedResult = optimizedParse(str);
    const time2 = performance.now() - start2;
    
    console.log(`Наивный парсер: ${naiveResult.success ? 'ПРИНЯТ' : 'ОТВЕРГ'} (x=${naiveResult.x}), время: ${time1.toFixed(2)}ms`);
    console.log(`Оптимизированный: ${optimizedResult.success ? 'ПРИНЯТ' : 'ОТВЕРГ'} (x=${optimizedResult.x}), время: ${time2.toFixed(2)}ms`);
    
    if (naiveResult.success !== optimizedResult.success) {
        console.error(`ОШИБКА: Парсеры расходятся!`);
        return false;
    }
    
    if (naiveResult.success && optimizedResult.success && naiveResult.x !== optimizedResult.x) {
        console.warn(`ВНИМАНИЕ: Разные значения x (${naiveResult.x} vs ${optimizedResult.x})`);
    }    
    console.log(`Ускорение: ${(time1 / time2).toFixed(2)}x`);
    return true;
}

function runRandomTests(numTests, stringLength) {
    console.log(`\n=== ЗАПУСК ${numTests} СЛУЧАЙНЫХ ТЕСТОВ (длина ${stringLength}) ===`);
    let passed = 0;
    let failed = 0;
    let totalNaiveTime = 0;
    let totalOptimizedTime = 0;
    for (let i = 0; i < numTests; i++) {
        const str = generateRandomString(stringLength);
        const start1 = performance.now();
        const naiveResult = naiveParse(str);
        const time1 = performance.now() - start1;
        const start2 = performance.now();
        const optimizedResult = optimizedParse(str);
        const time2 = performance.now() - start2;
        totalNaiveTime += time1;
        totalOptimizedTime += time2;
        if (naiveResult.success === optimizedResult.success) {
            passed++;
        } else {
            failed++;
            console.error(`\nТест ${i + 1} не пройден: "${str}"`);
            console.error(`Наивный: ${naiveResult.success ? 'ПРИНЯТ' : 'ОТВЕРГ'}`);
            console.error(`Оптимизированный: ${optimizedResult.success ? 'ПРИНЯТ' : 'ОТВЕРГ'}`);
        }
        if ((i + 1) % 10 === 0) {
            console.log(`Прогресс: ${i + 1}/${numTests} тестов...`);
        }
    }
    console.log(`\n=== РЕЗУЛЬТАТЫ ===`);
    console.log(`Пройдено: ${passed}/${numTests}`);
    console.log(`Не пройдено: ${failed}/${numTests}`);
    console.log(`Среднее время наивного: ${(totalNaiveTime / numTests).toFixed(2)}ms`);
    console.log(`Среднее время оптимизированного: ${(totalOptimizedTime / numTests).toFixed(2)}ms`);
    console.log(`Общее ускорение: ${(totalNaiveTime / totalOptimizedTime).toFixed(2)}x`);
    return failed === 0;
}
runRandomTests(20, 20);