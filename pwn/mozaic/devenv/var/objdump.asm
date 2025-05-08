
./bin/mozaic:     file format elf64-x86-64


Disassembly of section .text:

0000000000401000 <printHelp>:
  401000:	48 83 ec 08          	sub    rsp,0x8
  401004:	48 8d 3d f5 0f 00 00 	lea    rdi,[rip+0xff5]        # 402000 <read+0xdaf>
  40100b:	e8 d8 01 00 00       	call   4011e8 <printline>
  401010:	48 83 c4 08          	add    rsp,0x8
  401014:	c3                   	ret

0000000000401015 <parseCommand>:
  401015:	48 83 ec 08          	sub    rsp,0x8
  401019:	0f b6 07             	movzx  eax,BYTE PTR [rdi]
  40101c:	3c 68                	cmp    al,0x68
  40101e:	74 0b                	je     40102b <parseCommand+0x16>
  401020:	3c 71                	cmp    al,0x71
  401022:	74 16                	je     40103a <parseCommand+0x25>
  401024:	e8 bf 01 00 00       	call   4011e8 <printline>
  401029:	eb 0a                	jmp    401035 <parseCommand+0x20>
  40102b:	b8 00 00 00 00       	mov    eax,0x0
  401030:	e8 cb ff ff ff       	call   401000 <printHelp>
  401035:	48 83 c4 08          	add    rsp,0x8
  401039:	c3                   	ret
  40103a:	c7 06 01 00 00 00    	mov    DWORD PTR [rsi],0x1
  401040:	eb f3                	jmp    401035 <parseCommand+0x20>

0000000000401042 <loop>:
  401042:	55                   	push   rbp
  401043:	53                   	push   rbx
  401044:	48 83 ec 58          	sub    rsp,0x58
  401048:	c7 44 24 4c 00 00 00 	mov    DWORD PTR [rsp+0x4c],0x0
  40104f:	00 
  401050:	48 c7 04 24 00 00 00 	mov    QWORD PTR [rsp],0x0
  401057:	00 
  401058:	48 c7 44 24 08 00 00 	mov    QWORD PTR [rsp+0x8],0x0
  40105f:	00 00 
  401061:	48 c7 44 24 10 00 00 	mov    QWORD PTR [rsp+0x10],0x0
  401068:	00 00 
  40106a:	48 c7 44 24 18 00 00 	mov    QWORD PTR [rsp+0x18],0x0
  401071:	00 00 
  401073:	48 c7 44 24 20 00 00 	mov    QWORD PTR [rsp+0x20],0x0
  40107a:	00 00 
  40107c:	48 c7 44 24 28 00 00 	mov    QWORD PTR [rsp+0x28],0x0
  401083:	00 00 
  401085:	48 c7 44 24 30 00 00 	mov    QWORD PTR [rsp+0x30],0x0
  40108c:	00 00 
  40108e:	48 c7 44 24 38 00 00 	mov    QWORD PTR [rsp+0x38],0x0
  401095:	00 00 
  401097:	48 8d 2d 09 10 00 00 	lea    rbp,[rip+0x1009]        # 4020a7 <read+0xe56>
  40109e:	ba 03 00 00 00       	mov    edx,0x3
  4010a3:	48 89 ee             	mov    rsi,rbp
  4010a6:	bf 01 00 00 00       	mov    edi,0x1
  4010ab:	e8 80 01 00 00       	call   401230 <write>
  4010b0:	48 89 e7             	mov    rdi,rsp
  4010b3:	e8 68 00 00 00       	call   401120 <readline>
  4010b8:	48 8d 74 24 4c       	lea    rsi,[rsp+0x4c]
  4010bd:	48 89 e7             	mov    rdi,rsp
  4010c0:	e8 50 ff ff ff       	call   401015 <parseCommand>
  4010c5:	83 7c 24 4c 01       	cmp    DWORD PTR [rsp+0x4c],0x1
  4010ca:	75 d2                	jne    40109e <loop+0x5c>
  4010cc:	48 83 c4 58          	add    rsp,0x58
  4010d0:	5b                   	pop    rbx
  4010d1:	5d                   	pop    rbp
  4010d2:	c3                   	ret

00000000004010d3 <printBanner>:
  4010d3:	48 83 ec 08          	sub    rsp,0x8
  4010d7:	48 8d 3d 22 1f 00 00 	lea    rdi,[rip+0x1f22]        # 403000 <banner>
  4010de:	e8 05 01 00 00       	call   4011e8 <printline>
  4010e3:	48 83 c4 08          	add    rsp,0x8
  4010e7:	c3                   	ret

00000000004010e8 <_start>:
  4010e8:	48 83 ec 08          	sub    rsp,0x8
  4010ec:	b8 00 00 00 00       	mov    eax,0x0
  4010f1:	e8 dd ff ff ff       	call   4010d3 <printBanner>
  4010f6:	b8 00 00 00 00       	mov    eax,0x0
  4010fb:	e8 00 ff ff ff       	call   401000 <printHelp>
  401100:	b8 00 00 00 00       	mov    eax,0x0
  401105:	e8 38 ff ff ff       	call   401042 <loop>
  40110a:	bf 00 00 00 00       	mov    edi,0x0
  40110f:	e8 04 01 00 00       	call   401218 <exit>
  401114:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  40111b:	00 00 00 
  40111e:	66 90                	xchg   ax,ax

0000000000401120 <readline>:
  401120:	55                   	push   rbp
  401121:	53                   	push   rbx
  401122:	48 83 ec 48          	sub    rsp,0x48
  401126:	48 89 fb             	mov    rbx,rdi
  401129:	48 c7 04 24 00 00 00 	mov    QWORD PTR [rsp],0x0
  401130:	00 
  401131:	48 c7 44 24 08 00 00 	mov    QWORD PTR [rsp+0x8],0x0
  401138:	00 00 
  40113a:	48 c7 44 24 10 00 00 	mov    QWORD PTR [rsp+0x10],0x0
  401141:	00 00 
  401143:	48 c7 44 24 18 00 00 	mov    QWORD PTR [rsp+0x18],0x0
  40114a:	00 00 
  40114c:	48 c7 44 24 20 00 00 	mov    QWORD PTR [rsp+0x20],0x0
  401153:	00 00 
  401155:	48 c7 44 24 28 00 00 	mov    QWORD PTR [rsp+0x28],0x0
  40115c:	00 00 
  40115e:	48 c7 44 24 30 00 00 	mov    QWORD PTR [rsp+0x30],0x0
  401165:	00 00 
  401167:	48 c7 44 24 38 00 00 	mov    QWORD PTR [rsp+0x38],0x0
  40116e:	00 00 
  401170:	48 89 e5             	mov    rbp,rsp
  401173:	ba 40 00 00 00       	mov    edx,0x40
  401178:	48 89 ee             	mov    rsi,rbp
  40117b:	bf 00 00 00 00       	mov    edi,0x0
  401180:	e8 cc 00 00 00       	call   401251 <read>
  401185:	48 89 e8             	mov    rax,rbp
  401188:	48 8d 4c 24 40       	lea    rcx,[rsp+0x40]
  40118d:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401194:	00 00 00 00 
  401198:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  40119f:	00 
  4011a0:	0f b6 10             	movzx  edx,BYTE PTR [rax]
  4011a3:	80 fa 0a             	cmp    dl,0xa
  4011a6:	74 11                	je     4011b9 <readline+0x99>
  4011a8:	88 13                	mov    BYTE PTR [rbx],dl
  4011aa:	48 83 c3 01          	add    rbx,0x1
  4011ae:	48 83 c0 01          	add    rax,0x1
  4011b2:	48 39 c8             	cmp    rax,rcx
  4011b5:	75 e9                	jne    4011a0 <readline+0x80>
  4011b7:	eb ba                	jmp    401173 <readline+0x53>
  4011b9:	c6 03 00             	mov    BYTE PTR [rbx],0x0
  4011bc:	48 83 c4 48          	add    rsp,0x48
  4011c0:	5b                   	pop    rbx
  4011c1:	5d                   	pop    rbp
  4011c2:	c3                   	ret

00000000004011c3 <stringlen>:
  4011c3:	80 3f 00             	cmp    BYTE PTR [rdi],0x0
  4011c6:	74 1a                	je     4011e2 <stringlen+0x1f>
  4011c8:	48 89 f8             	mov    rax,rdi
  4011cb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  4011d0:	48 89 c2             	mov    rdx,rax
  4011d3:	48 83 c0 01          	add    rax,0x1
  4011d7:	80 38 00             	cmp    BYTE PTR [rax],0x0
  4011da:	75 f4                	jne    4011d0 <stringlen+0xd>
  4011dc:	29 fa                	sub    edx,edi
  4011de:	8d 42 02             	lea    eax,[rdx+0x2]
  4011e1:	c3                   	ret
  4011e2:	b8 01 00 00 00       	mov    eax,0x1
  4011e7:	c3                   	ret

00000000004011e8 <printline>:
  4011e8:	53                   	push   rbx
  4011e9:	48 89 fb             	mov    rbx,rdi
  4011ec:	e8 d2 ff ff ff       	call   4011c3 <stringlen>
  4011f1:	89 c2                	mov    edx,eax
  4011f3:	48 89 de             	mov    rsi,rbx
  4011f6:	bf 01 00 00 00       	mov    edi,0x1
  4011fb:	e8 30 00 00 00       	call   401230 <write>
  401200:	ba 01 00 00 00       	mov    edx,0x1
  401205:	48 8d 35 9f 0e 00 00 	lea    rsi,[rip+0xe9f]        # 4020ab <read+0xe5a>
  40120c:	bf 01 00 00 00       	mov    edi,0x1
  401211:	e8 1a 00 00 00       	call   401230 <write>
  401216:	5b                   	pop    rbx
  401217:	c3                   	ret

0000000000401218 <exit>:
  401218:	89 fa                	mov    edx,edi
  40121a:	b8 3c 00 00 00       	mov    eax,0x3c
  40121f:	0f 05                	syscall
  401221:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  401228:	00 00 00 
  40122b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000401230 <write>:
  401230:	55                   	push   rbp
  401231:	48 89 e5             	mov    rbp,rsp
  401234:	89 7d fc             	mov    DWORD PTR [rbp-0x4],edi
  401237:	48 89 75 f0          	mov    QWORD PTR [rbp-0x10],rsi
  40123b:	89 55 f8             	mov    DWORD PTR [rbp-0x8],edx
  40123e:	b8 01 00 00 00       	mov    eax,0x1
  401243:	8b 7d fc             	mov    edi,DWORD PTR [rbp-0x4]
  401246:	48 8b 75 f0          	mov    rsi,QWORD PTR [rbp-0x10]
  40124a:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
  40124d:	0f 05                	syscall
  40124f:	5d                   	pop    rbp
  401250:	c3                   	ret

0000000000401251 <read>:
  401251:	55                   	push   rbp
  401252:	48 89 e5             	mov    rbp,rsp
  401255:	89 7d fc             	mov    DWORD PTR [rbp-0x4],edi
  401258:	48 89 75 f0          	mov    QWORD PTR [rbp-0x10],rsi
  40125c:	89 55 f8             	mov    DWORD PTR [rbp-0x8],edx
  40125f:	b8 00 00 00 00       	mov    eax,0x0
  401264:	8b 7d fc             	mov    edi,DWORD PTR [rbp-0x4]
  401267:	48 8b 75 f0          	mov    rsi,QWORD PTR [rbp-0x10]
  40126b:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
  40126e:	0f 05                	syscall
  401270:	5d                   	pop    rbp
  401271:	c3                   	ret
