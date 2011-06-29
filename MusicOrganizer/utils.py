import shutil;
import platform;
import os;
import sys;
try:
	import stagger;
except ImportError:
	sys.path.insert(0, sys.path[0] + '/MusicOrganizer/stagger/');
	import stagger;

#
# Copyright (c) by Patryk Jaworski
# Contact:
# -> E-mail: Patryk Jaworski <skorpion9312@gmail.com>
# -> XMPP/Jabber: skorpion9312@jabber.org
#

# Global variables
ENABLE_VERBOSE = False;
DIR_SEPARATOR = '/'
BAD_CHARS = '!@#?+=\'"[]|`$%^&*<>/\\{};~'
REPLACE_WITH = '';

def init():
	"""
	Do some initialize actions
	"""
	global DIR_SEPARATOR;
	if platform.system().lower() == 'windows':
		DIR_SEPARATOR = '\\';

def moveCovers(covers, outputDir, copy):
	"""
	Move all covers to outputDir
	"""
	if outputDir[-1] != DIR_SEPARATOR:
		outputDir += DIR_SEPARATOR;
	i = 1;
	num = 0;
	for c in covers:
		ext = c[c.rfind('.'):];
		output = outputDir + 'cover' + ext;
		if c != output:
			while os.path.exists(output):
				output = outputDir + 'cover-' + str(i) + ext;
				i += 1;
			if copy:
				verbose(_('Copying cover %s -> %s') % (c, output));
				shutil.copy2(c, output);
			else:
				verbose(_('Moving cover %s -> %s') % (c, output));
				shutil.move(c, output);	
			num += 1;
		else:
			verbose(_('Skipping %s') % c);
	return num;

def verbose(message):
	"""
	Print verbose messages
	"""
	global ENABLE_VERBOSE;
	if ENABLE_VERBOSE:
		print('[V] %s' % message);

def getTag(track, returnNone = False):
	"""
	Get ID3 tags from track
	"""
	oldName = os.path.basename(track);
	try:
		tag = stagger.read_tag(track);
		tags = {'artist':tag.artist or 'Unknown artist', 
		'album':tag.album or 'Unknown album', 
		'date':tag.date or 'XXXX', 
		'title':tag.title or 'Unknown title', 
		'genre':tag.genre or 'Unknown genre', 
		'track':tag.track or 'XX',
		'old-file-name':oldName[0:oldName.rfind('.')]};
	except stagger.errors.NoTagError:
		print('[W] %s' % _('Track %s has no ID3 tags...' % track));
		if returnNone:
			return None;
		tags = getDefaultTag();
	return tags;

def getDefaultTag(track):
	oldName = os.path.basename(track);
	return {'artist':'Unknown artist', 
	'album':'Unknown album', 
	'date':'XXXX', 
	'title':'Unknown title', 
	'genre':'Unknown genre', 
	'track':'XX',
	'old-file-name':oldName[0:oldName.rfind('.')]};

def normalizeTags(tags):
	"""
	Characters in tags which need to be replaced are in global variable BAD_CHARS
	Characters with which you want replace BAD_CHARS are in global variable REPLACE_WITH
	"""
	global BAD_CHARS;
	global REPLACE_WITH;
	for tag in tags:
		for b in BAD_CHARS:
			tags[tag] = str(tags[tag]).replace(b, REPLACE_WITH);
		if not tags[tag]:
			tags[tag] = 'empty';
	return tags;

def moveTrack(track, tags, target, scheme, copy=False):
	"""
	Move track to target using scheme
	"""
	global DIR_SEPARATOR;
	output = target + scheme.format(**tags) + track[-4:].lower();
	outputDir = os.path.dirname(output);
	if not os.path.exists(outputDir):
		verbose(_('Creating output directories...'));
		os.makedirs(outputDir);
	i = 1;
	ext = output[output.rfind('.'):];
	name = os.path.basename(output[0:output.rfind('.')]);
	if track != output:
		while os.path.exists(output):
			output = outputDir + DIR_SEPARATOR + name + '-' + str(i) + ext;
			i += 1;
		if copy:
			verbose(_('Copying %s -> %s') % (track, output));
			shutil.copy2(track, output);
			return True;
		else:
			verbose(_('Moving %s -> %s') % (track, output));
			shutil.move(track, output);
			return True;
	else:
		verbose(_('Skipping %s...') % track)
		return False;

def prepare(path, target):
	"""
	Prepare input/output directories
	"""
	if not path or not target:
		raise Exception(_('Please specify search and target directories!'));
	verbose(_('Preparing directories...'));
	verbose(_('Checking path...'));
	if not os.path.exists(path):
		raise Exception(_('Directory given in path does not exists!'));
	if not os.access(path, os.R_OK):
		raise Exception(_('Directory given in path has no READ privilages!'));
	verbose(_('Checking target dir...'));
	if not os.path.exists(target):
		verbose(_('Directory %s not found, trying to create...') % target);
		try:
			os.mkdir(target);
		except OSError:
			raise Exception(_('Unable to create directory...'));
	verbose(_('Checking access in target directory...'));
	if not os.access(target, os.W_OK):
		raise Exception(_('Target directory is not writable!'));

def getHomeDir():
	return os.path.expanduser('~');

def getVersion():
	try:
		vfp = open('VERSION', 'r');
		version = vfp.read();
		vfp.close();
		if not version:
			raise Exception();
		return version.strip();
	except:
		return _('Unknown');

def initGettext():
	import gettext;
	gettext.install('music-organizer', 'locale');
