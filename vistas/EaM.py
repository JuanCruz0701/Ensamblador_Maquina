class Compiler:
    def __init__(self):
        self.machine_code = []  # Lista para almacenar las instrucciones en código máquina
        self.label_map = {}  # Mapa para almacenar las etiquetas y sus posiciones
        self.asm_code = []  # Lista para almacenar el código ensamblador
        self.memory_address = 0x00400000  # Dirección inicial de las instrucciones

    def assemble_to_machine_code(self, asm_code):
        # Recorrer cada línea del código ensamblador y convertirla a hexadecimal
        self.machine_code = []
        self.asm_code = asm_code.splitlines()  # se dividen las lineas del codigo
        
        # Primera pasada para calcular la dirección de las etiquetas
        self.first_pass_labels()

        # Segunda pasada para convertir el ensamblador en código máquina
        for instruction in self.asm_code:
            machine_instr = self.convert_instruction_to_machine(instruction.strip())
            if machine_instr:
                self.machine_code.append(machine_instr)
                
        # Agregar la instrucción "ac0a0050" al final de machine_code
        #self.machine_code.append("ac0a0050")
        return '\n'.join(self.machine_code)

    def first_pass_labels(self):
        # Recorrer el código para encontrar etiquetas y asignarles direcciones
        current_address = self.memory_address
        for line in self.asm_code:
            line = line.strip()
            if line.endswith(":"):  # Si es una etiqueta
                label = line[:-1]  # Quitar el :
                self.label_map[label] = current_address
            else:
                current_address += 4  # Aumentar la dirección por cada instrucción

    def convert_instruction_to_machine(self, instruction):
        # Asignar los opcodes para las instrucciones conocidas
        opcodes = {
            'addi': '001000',  # Tipo I
            'beq':  '000100',  # Tipo I
            'bne':  '000101',  # Tipo I
            'lw':   '100011',  # Tipo I
            'sw':   '101011',  # Tipo I
            'j':    '000010',  # Tipo J
            'add':  '000000',  # Tipo R 
            'sub':  '000000',  # Tipo R
            'slt':  '000000',  # Tipo R
            'and':  '000000',  # Tipo R
            'or':   '000000',  # Tipo R
        }

        # Separar la instrucción y los operandos
        parts = instruction.split()
        if len(parts) == 0:
            return None  # Línea vacía o no soportada

        instr = parts[0]  # Instrucción
        operands = parts[1:]  # Operandos

        # Convertir a código máquina según el tipo de instrucción
        if instr in opcodes:
            opcode = opcodes[instr]

            # Instrucciones R-type
            if instr in ['add', 'sub', 'slt', 'and', 'or']:
                return self.assemble_r_type(opcode, instr, operands)

            # Instrucciones I-type
            elif instr in ['addi', 'beq', 'bne', 'lw', 'sw']:
                return self.assemble_i_type(opcode, instr, operands)

            # Instrucciones J-type
            elif instr == 'j':
                # Manejo de etiquetas en instrucciones j
                if operands[0] in self.label_map:
                    address = self.label_map[operands[0]]
                else:
                    raise ValueError(f"Etiqueta desconocida: {operands[0]}")

                return self.assemble_j_type(opcode, address)

        return None  # Instrucción no soportada.

    def assemble_r_type(self, opcode, instr, operands):
        # Formato R: opcode (6 bits), rs (5 bits), rt (5 bits), rd (5 bits), shamt (5 bits), funct (6 bits)
        funct_codes = {
            'add': '100000',
            'sub': '100010',
            'slt': '101010',
            'and': '100100',
            'or':  '100101',

        }

        rd = self.get_register_bin(operands[0])  # Destino
        rs = self.get_register_bin(operands[1])  # Primer operando
        rt = self.get_register_bin(operands[2])  # Segundo operando
        shamt = '00000'  # No hay shift en add/sub/slt

        funct = funct_codes[instr]

        # Concatenar todo para formar la instrucción
        binary_instr = opcode + rs + rt + rd + shamt + funct
        return self.bin_to_hex(binary_instr)

    def assemble_i_type(self, opcode, instr, operands):
         # Formato I: opcode (6 bits), rs (5 bits), rt (5 bits), immediate (16 bits)
        rt = self.get_register_bin(operands[0])  # Destino o registro de comparación

        # Manejo para lw y sw
        if instr in ['lw', 'sw']:
            # Extraer el formato imm(rs)
            imm_and_rs = operands[1]
            imm, rs = imm_and_rs.split('(')
            imm = imm.strip()  # El inmediato
            rs = rs.strip(')')  # El registro base

            # Convertir registro base y inmediato
            rs_bin = self.get_register_bin(rs)  # Base (registro)
            imm_bin = self.get_immediate_bin(imm)  # Inmediato
        elif instr in ['beq', 'bne']:  # Si es una instrucción de salto condicional
            label = operands[2]
            if label in self.label_map:
                label_address = self.label_map[label]
                current_address = self.memory_address
                # Calcular el offset para el salto
                offset = (label_address - current_address) // 4
                imm_bin = format(offset & 0xFFFF, '016b')  # Immediate de 16 bits
            else:
                raise ValueError(f"Etiqueta desconocida: {label}")
            rs_bin = self.get_register_bin(operands[1])  # Primer operando
        else:
            # Para otras instrucciones de tipo I
            rs_bin = self.get_register_bin(operands[1])  # Primer operando
            imm_bin = self.get_immediate_bin(operands[2])  # Inmediato

        # Construir la instrucción binaria
        binary_instr = opcode + rs_bin + rt + imm_bin
        return self.bin_to_hex(binary_instr)

    def assemble_j_type(self, opcode, label):
        # Formato J: opcode (6 bits), address (26 bits)
        address = format(int(label), '026b')  # Convertir la etiqueta a binario de 26 bits
        binary_instr = opcode + address
        return self.bin_to_hex(binary_instr)

    def get_register_bin(self, reg):
        # Eliminar cualquier coma u otro símbolo y limpiar el registro
        reg = reg.replace(',', '').strip()

        # Mapa de registros a su número en binario (5 bits)
        reg_map = {
            '$0': 0, '$zero': 0,
            '$at': 1,
            '$v0': 2, '$v1': 3,
            '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
            '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
            '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
            '$t8': 24, '$t9': 25,
            '$k0': 26, '$k1': 27,
            '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
        }

        reg_num = reg_map.get(reg, None)
        if reg_num is None:
            raise ValueError(f"Registro desconocido: {reg}")
        return format(reg_num, '05b')  # Retorna el número del registro en binario de 5 bits.

    def get_immediate_bin(self, imm):
        # Convierte el inmediato a binario de 16 bits
        return format(int(imm), '016b')

    def bin_to_hex(self, binary_instr):
        # Convierte la instrucción binaria a hexadecimal
        hex_instr = hex(int(binary_instr, 2))[2:].zfill(8)  # Asegurarse de que tenga 8 dígitos
        return hex_instr
    
def Codigo():
    return """
    """

compiler = Compiler()
asm_code = Codigo()
machine_code = compiler.assemble_to_machine_code(asm_code)


#file_path = "C:/Users/Juan/Documents/Documentos_para_residencia/RESIDENCIA/MIPS_7_SEG/src/memfile.dat" 

#with open(file_path, 'w') as file:
#    file.write(machine_code)

#print(f"Código máquina guardado en {file_path}")