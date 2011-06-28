from . import interface;
from .. import utils as utils;
import getopt;
import sys;
import os;

#
# Copyright (c) by Patryk Jaworski
# Contact:
# -> E-mail: Patryk Jaworski <skorpion9312@gmail.com>
# -> XMPP/Jabber: skorpion9312@jabber.org
#

class Organizer(interface.Interface):
	__args = [];
	__sep = '/';
	__path = '';
	__target = '';
	__verbose = False;
	__recursive = False;
	__copy = False;
	__delete = False;
	__follow = False;
	__force = False;
	__scheme = '{title}';
	__recognizeCovers = False;
	__numOk = 0;
	__numSkipped = 0;

	def __init__(self, args):
		self.__args = args;
		# Initialize utils
		utils.init();
		self.__parseOptions();

	def __parseOptions(self):
		self.__scheme = '{artist}{0}{album}{0}{title}'.replace('{0}', utils.DIR_SEPARATOR);
		try:
			options, args = getopt.getopt(self.__args[1:], 'p:rdft:chvs:', ['path=', 'target-directory=', 'scheme=', 'delete', 'force', 'recursive', 'verbose', 'copy', 'help', 'recognize-covers', 'follow']);
			for option, value in options:
				if option in ('-h', '--help'):
					self.__usage();
					sys.exit(0);
				elif option in ('-p', '--path'):
					if value[-1] != utils.DIR_SEPARATOR:
						value += utils.DIR_SEPARATOR;
					utils.verbose('Setting path as %s...' % value);
					self.__path = value;
				elif option in ('-t', '--target-directory'):
					if value[-1] != utils.DIR_SEPARATOR:
						value += utils.DIR_SEPARATOR;
					utils.verbose('Setting target as %s...' % value);
					self.__target = value;
				elif option in ('-f', '--force'):
					utils.verbose('Setting option force...');
					self.__force = True;
				elif option in ('-d', '--delete'):
					utils.verbose('Setting option delete...');
					self.__delete = True;
				elif option in ('-v', '--verbose'):
					utils.ENABLE_VERBOSE = True;
				elif option in ('-r', '--recursive'):
					utils.verbose('Setting option recursive...');
					self.__recursive = True;
				elif option in ('-c', '--copy'):
					utils.verbose('Setting option copy...');
					self.__copy = True;
				elif option in ('-s', '--scheme'):
					utils.verbose('Setting scheme: %s...' % value);
					self.__scheme = value;
				elif option == '--recognize-covers':
					utils.verbose('Setting option recognize-covers...');
					self.__recognizeCovers = True;
				elif option == '--follow':
					self.__follow = True;
		except getopt.GetoptError as err:
			print('[E] Bad options...');
			self.__usage();
			sys.exit(1);
		if not self.__path:
			self.__path = '.%s' % utils.DIR_SEPARATOR;
			print('[I] Using default path: %s...' % self.__path);
		if not self.__target:
			self.__target = '.%smusic-organizer%s' % (utils.DIR_SEPARATOR, utils.DIR_SEPARATOR);
			print('[I] Using default target: %s...' % self.__target);
	
	def operate(self):
		self.__organize(self.__path);
		self.__summary();
	
	def __summary(self):
		print('');
		print(' Summary '.center(50, '='));
		print('%s files: %d' % ('Copied' if self.__copy else 'Moved', self.__numOk));
		print('Skipped files: %d' % (self.__numSkipped));
		print((' :-%s ' % (')' if self.__numOk > 0 else '(')).center(50, '='));
		print('');
	
	def __organize(self, path):
		try:
			files = os.listdir(path);
			if len(files) == 0:
				print("[W] Directory %s is empty..." % path);
		except OSError:
			print('[W] Cannot list directory %s...' % path);
			return;
		covers = [];
		lastTag = None;
		for f in files:
			if os.path.islink(path + f) and not self.__follow:
				self.v('Skipping link %s...' % (path + f));
				continue;
			if os.path.isdir(path + f) and self.__recursive:
				self.__organize(path + f + utils.DIR_SEPARATOR);
				continue;
			if f[-4:].lower() == '.mp3':
				lastTag = utils.getTag(path + f);
				if utils.moveTrack(path + f, lastTag, self.__target, self.__scheme, self.__copy):
					self.__numOk += 1;
				else:
					self.__numSkipped += 1;
			if self.__recognizeCovers:
				if f[f.rfind('.'):].lower() in ('.jpg', '.gif', '.png', '.bmp', '.jpeg'):
					covers.append(path + f);
		if lastTag != None and len(covers) != 0:
			outputDir = self.__target + self.__scheme.format(**lastTag);
			utils.moveCovers(covers, outputDir, self.__copy)
		if not self.__copy and self.__delete and path != self.__path:
			try:
				utils.verbose('Removing %s' % path);
				os.rmdir(path);
			except Exception as err:
				utils.verbose('I can\'t remove  %s' % path);
				try:
					if self.__force:
						utils.v('Force removing %s' % path);
						os.rmdirs(path);
					else:
						raise Exception();
				except:
					print('[W] Unable to remove directory %s...' % path);

	def __usage(self):
		print('========== MUSIC-ORGANIZER %s  ==========' % utils.getVersion());
		print('Automatically organize, sort or rename your mp3 music collection\n');
		print('Authors:');
		print('   -> Patryk Jaworski <skorpion9312@gmail.com>\n   -> Ariana Las <ariana.las@gmail.com>');
		print('\nOutput style:');
		print('[E] <- Error\n[W] <- Warning\n[V] <- Verbose\n[I] <- Information\n');
		print('Usage:');
		print('   $ music-organizer - start with GUI mode');
		print('   $ music-organizer [OPTIONS] - start with text mode');
		print('\nOptions:\n   -t --target-directory\n      specify target directory (required)');
		print('   -p --path\n      specify search directory (required)');
		print('   -d --delete\n      delete directories after all files are moved');
		print('   -f --force\n      force remove unnecessary directories');
		print('   -r --recursive\n      search in directories recursively');
		print('   -c --copy\n      copy files instead of moving');
		print('   -s --scheme\n      specify output files scheme');
		print('       default: {artist}/{album}/{title}');
		print('       available: {artist} {album} {date} {title}\n                  {old-file-name} {genre} {track}');
		print('   -h --help\n      display help');
		print('   -v --verbose\n      enable verbose messages (should be first option)');
		print('   --recognize-covers\n      move/copy all image files');
		print('   --follow\n      follow symlinks');
		print('\nExamples:\n   $ music-organizer -p ~/Music/ -t ~/Music/ -r --recognize-covers');
		print('      Organize ~/Music/ directory (do not remove old directories even empty)');
		print('\n   $ music-organizer -p ~/ -t ~/Music/ -r -d');
		print('      Find all music (mp3) files in your home directory and move them to ~/Music/\n      (use default scheme)');
