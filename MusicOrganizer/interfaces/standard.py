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
					utils.verbose(_('Setting path as %s...') % value);
					self.__path = value;
				elif option in ('-t', '--target-directory'):
					if value[-1] != utils.DIR_SEPARATOR:
						value += utils.DIR_SEPARATOR;
					utils.verbose(_('Setting target as %s...') % value);
					self.__target = value;
				elif option in ('-f', '--force'):
					utils.verbose(_('Setting option force...'));
					self.__force = True;
				elif option in ('-d', '--delete'):
					utils.verbose(_('Setting option delete...'));
					self.__delete = True;
				elif option in ('-v', '--verbose'):
					utils.ENABLE_VERBOSE = True;
				elif option in ('-r', '--recursive'):
					utils.verbose(_('Setting option recursive...'));
					self.__recursive = True;
				elif option in ('-c', '--copy'):
					utils.verbose(_('Setting option copy...'));
					self.__copy = True;
				elif option in ('-s', '--scheme'):
					utils.verbose(_('Setting scheme: %s...') % value);
					self.__scheme = value;
				elif option == '--recognize-covers':
					utils.verbose(_('Setting option recognize-covers...'));
					self.__recognizeCovers = True;
				elif option == '--follow':
					self.__follow = True;
		except getopt.GetoptError as err:
			print('[E] %s' % _('Bad options...'));
			self.__usage();
			sys.exit(1);
		if not self.__path:
			self.__path = '.%s' % utils.DIR_SEPARATOR;
			print('[I] %s' % _('Using default path: %s...') % self.__path);
		if not self.__target:
			self.__target = '.%smusic-organizer%s' % (utils.DIR_SEPARATOR, utils.DIR_SEPARATOR);
			print('[I] %s' % _('Using default target: %s...') % self.__target);
	
	def operate(self):
		self.__organize(self.__path);
		self.__summary();
	
	def __summary(self):
		print('');
		print(_(' Summary ').center(50, '='));
		print(_('%s files: %d') % (_('Copied') if self.__copy else _('Moved'), self.__numOk));
		print(_('Skipped files: %d') % (self.__numSkipped));
		print((' :-%s ' % (')' if self.__numOk > 0 else '(')).center(50, '='));
		print('');
	
	def __organize(self, path):
		try:
			files = os.listdir(path);
			if len(files) == 0:
				print('[W] %s' % _('Directory %s is empty...') % path);
		except OSError:
			print('[W] %s' % _('Cannot list directory %s...') % path);
			return;
		covers = [];
		lastTag = None;
		for f in files:
			if os.path.islink(path + f) and not self.__follow:
				self.v(_('Skipping link %s...') % (path + f));
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
				utils.verbose(_('Removing %s') % path);
				os.rmdir(path);
			except Exception as err:
				utils.verbose(_('I can\'t remove %s') % path);
				try:
					if self.__force:
						utils.v(_('Force removing %s') % path);
						os.rmdirs(path);
					else:
						raise Exception();
				except:
					print('[W] %s' % _('Unable to remove directory %s...') % path);

	def __usage(self):
		print('========== MUSIC-ORGANIZER %s  ==========' % utils.getVersion());
		print(_('Automatically organize, sort or rename your mp3 music collection') + '\n');
		print(_('Authors:'));
		print('   -> Patryk Jaworski <skorpion9312@gmail.com>\n   -> Ariana Las <ariana.las@gmail.com>');
		print('');
		print(_('Output style:'));
		print('[E] <- %s\n[W] <- %s\n[V] <- %s\n[I] <- %s\n' % (_('Error'), _('Warning'), _('Verbose'), _('Information')));
		print(_('Usage:'));
		print('$ music-organizer - %s ' % _('start with GUI mode'));
		print('$ music-organizer [OPTIONS] - %s' % _('start with text mode'));
		print('');
		print(_('Options:'));
		print('   -t --target-directory')
		print('      ' + _('specify target directory (required)'));
		print('   -p --path')
		print('      ' + _('specify search directory (required)'));
		print('   -d --delete')
		print('      ' + _('delete directories after all files are moved'));
		print('   -f --force')
		print('      ' + _('force remove unnecessary directories'));
		print('   -r --recursive')
		print('      ' + _('search in directories recursively'));
		print('   -c --copy')
		print('      ' + _('copy files instead of moving'));
		print('   -s --scheme')
		print('      ' + _('specify output files scheme'));
		print('       %s: {artist}/{album}/{title}' % _('default'));
		print('       %s: {artist} {album} {date} {title}\n      {old-file-name} {genre} {track}' % _('available'));
		print('   -h --help')
		print('      ' + _('display help'));
		print('   -v --verbose')
		print('      ' + _('enable verbose messages (should be first option)'));
		print('   --recognize-covers')
		print('      ' + _('move/copy all image files'));
		print('   --follow')
		print('    ' + _('follow symlinks'));
		print('');
		print(_('Examples:'))
		print('   $ music-organizer -p ~/Music/ -t ~/Music/ -r --recognize-covers');
		print('      ' + _('Organize ~/Music/ directory (do not remove old directories even empty)'));
		print('\n   $ music-organizer -p ~/ -t ~/Music/ -r -d');
		print('      ' + _('Find all music (mp3) files in your home directory and move them to ~/Music/      (use default scheme)'));
