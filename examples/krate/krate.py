#
numbers = [str(x) for x in range(32)]
letters = [chr(x) for x in range(97, 123)]
crate = '''
sandbox crate

map {boot: @init}
/*initialize utility vars and register vars*/
service init {
    writer = 0
    alpha = 0
    beta = 0
    status = 0'''
for letter in letters:
    crate += '\n    ' + letter + ' = 0'
crate += '''
}

/*map operator service to exec jump table*/

map {
    copy: @copy
    add: @add
    sub: @sub
    not: @not
    or: @or
    and: @and
    eq: @eq
    ne: @ne
    gt: @gt
    lt: @lt
    gte: @gte
    lte: @lte
    unary: @status_alpha
}

service copy { @status_zero alpha = beta @writer}

service add { @status_zero alpha = alpha + beta @writer}

service sub { @status_zero alpha = alpha - beta  @writer}

service not { @status_zero alpha = !beta  @writer}

service or { @status_zero alpha = alpha | beta  @writer}

service and { @status_zero alpha = alpha & beta @writer}

service eq { @status_zero if (alpha == beta) {[true]} else {[false]}}

service ne { @status_zero if (alpha != beta) {[true]} else {[false]}}

service gt { @status_zero if (alpha > beta) {[true]} else {[false]}}

service lt { @status_zero if (alpha < beta) {[true]} else {[false]}}

service gte { @status_zero if (alpha >= beta) {[true]} else {[false]}}

service lte { @status_zero if (alpha <= beta) {[true]} else {[false]}}

service status_zero {
    status = 0
}

service status_alpha {
    status = 1
}

service status_beta {
    status = 2
}

service writer {
    jump (writer) {'''
for letter in letters:
    crate += '{ ' + letter + ' = alpha } '
crate += '''}
}

map {jump: @jump}
service jump {
    jump (z) {'''
for number in numbers:
    crate += '{ [ jump' + number + '] } '
crate += '''}
}


map {printme : @printme}
service printme { ['''
for number in numbers:
    crate += '''alias jump''' + number + ''' echo ''' + number + ''';'''
crate += '''jump]
}'''
for letter in letters:
    crate += '''
map {''' + letter + ' : @' + letter + '''}
service ''' + letter + ''' { jump (status) {
        { alpha = ''' + letter + ''' @status_alpha}
        { beta = ''' + letter + ''' @status_beta}
        { writer = ''' + str(ord(letter) - 97) + ''' }
    }  
}'''
for number in numbers:
    crate += '''
map {delete''' + number + ' : @delete' + number + '''}
service delete''' + number + ''' { jump (status) {
        { alpha = ''' + number + ''' @status_alpha}
        { beta = ''' + number + ''' @status_beta}
        { }
    }
}'''

print(crate)
