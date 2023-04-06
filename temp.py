

# workers = 3
# imagenum = 11

# assignments = [0]*workers
# for x in range(workers):
#     main = imagenum//workers
#     if main < imagenum:

#         assignments[x] = main
#     else:
#         assignments[x] = imagenum
#     workers -= 1
#     imagenum -= main
    
# print(assignments,sum(assignments))

l = "abcdefghijklmnopqrstuvwxyz"
print(l[1:][::2])
