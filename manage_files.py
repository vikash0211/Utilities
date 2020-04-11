import os
import stat
import hashlib
import argparse

class Files:

    def __init__(self, path):

        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        self.files_dict = {}
        self.files_md5_dict = {}
        self.files_count = 0

    def print_files(self):

        i = 0
        for path, subdirs, files in os.walk(self.path):
            for name in files:
                i += 1
                curr_file = os.path.join(path, name)
                print('{}. {}'.format(i, curr_file))

        self.files_count += 1

    def find_duplicate_by_name(self, show = False, delete = False):

        i = 0
        for path, subdirs, files in os.walk(self.path):
            for name in files:
                curr_file = os.path.join(path, name)
                if not os.access(curr_file, os.R_OK):
                    continue
                if not self.files_dict.get(name):
                    self.files_dict[name] = []
                    self.files_dict[name].append(curr_file)
                    continue

                chksum_curr_file = hashlib.md5(open(curr_file,'rb').read()).hexdigest()
                for f in self.files_dict[name]:
                    if chksum_curr_file != hashlib.md5(open(f,'rb').read()).hexdigest():
                        continue
                    break
                else:
                    self.files_dict[name].append(curr_file)
                    continue

                i += 1
                if show:
                    print('{}. {}'.format(i, curr_file))
                    print('   {}'.format(f))

                if delete:
                    self.delete_file(curr_file)

    def find_duplicate_by_content(self, show = False, delete = False):

        i = 0
        for path, subdirs, files in os.walk(self.path):
            for name in files:
                curr_file = os.path.join(path, name)
                if not os.access(curr_file, os.R_OK):
                    continue

                chksum_curr_file = hashlib.md5(open(curr_file,'rb').read()).hexdigest()
                for f, chksum in self.files_md5_dict.items():
                    if chksum_curr_file != chksum:
                        continue
                    break
                else:
                    self.files_md5_dict[curr_file] = chksum_curr_file
                    continue

                i += 1
                if show:
                    print('{}. {}'.format(i, curr_file))
                    print('   {}'.format(f))

                if delete:
                    self.delete_file(curr_file)

    def delete_file(self, file):

        if not os.access(file, os.W_OK):
            os.chmod(file, stat.S_IWRITE)
        try:
            os.remove(file)
        except Exception as e:
            print('   {} : FAILED. Exception: {}'.format(file, e))
        else:
            print('   {} : DELETED'.format(file))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Find and Delete Duplicate Files")
    parser.add_argument('--path', required = True, help = "Directory Path to search for Duplicate Files")
    parser.add_argument('-p', '--print_files', action='store_true', help = "Print Files")
    parser.add_argument('-P', '--print_duplicate', action='store_true', help = "Print Duplicate Files")
    parser.add_argument('-D', '--delete_duplicate', action='store_true', help = "Delete Duplicate Files")
    parser.add_argument('-C', '--compare_by_content', action='store_true', help = "Compare File by Content")
    args, unknown = parser.parse_known_args()

    files = Files(args.path)
    if args.print_files:
        files.print_files()
    if not args.compare_by_content:
        files.find_duplicate_by_name(show = args.print_duplicate, delete = args.delete_duplicate)
    else:
        files.find_duplicate_by_content(show = args.print_duplicate, delete = args.delete_duplicate)
