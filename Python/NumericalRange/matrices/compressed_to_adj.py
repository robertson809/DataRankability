import sys
import heapq


def main():
    name = sys.argv[1]
    infile = open(name)
    outfile = open(name[:-4] + '_cleaned_adj_mat.txt', 'w+')
    line_list = infile.readlines()

    n = int(line_list[0][0])

    for line in line_list:  # support for cleaning up to degree, and size n = 10
        # print('original line is', line)
        if len(line) == 4:  # empty graph
            line = []
        elif line[3] == ' ':
            # print(line[3], 'this is the normal case')
            line = line[4:]
        elif line[4] == ' ':
            print('this is the case where the degree is between 10 and 100')
            line = line[5:]
        elif line[5] == ' ':
            print('this is the case where the degree is between 100 and 1000')
            line = line[6:]
        elif line[6] == ' ':
            line = line[7:]
        else:
            raise ValueError("degree craaazzzy high bro, add another line up there and"
                             "you should be go tho")
        adj_lists_dict = dict((i, []) for i in range(n))
        # print('line is', line, end='')
        for i in range(0, len(line), 4):
            # print(line[i], end='')
            # print('They are is', int(line[i]), int(line[i + 2]))
            adj_lists_dict[int(line[i])].append(int(line[i + 2]))
        # print(adj_lists_dict)
        # print()

        for key in adj_lists_dict.keys():
            adj_line = ''
            adj_list = adj_lists_dict[key]
            if not adj_list:  # checks if its empty
                for i in range(n - 1):
                    adj_line += '0 '
                adj_line += '0'

            else:
                heapq.heapify(adj_list)
                cur = heapq.heappop(adj_list)
                for i in range(n - 1):
                    if i != cur:
                        adj_line += '0 '
                    else:
                        adj_line += '1 '
                        if adj_list:  # makes sure it's not empty before popping
                            cur = heapq.heappop(adj_list)
                if n - 1 != cur:
                    adj_line += '0'
                else:
                    adj_line += '1'
            outfile.write(adj_line + '\n')
        outfile.write('\n')


if __name__ == '__main__':
    main()
