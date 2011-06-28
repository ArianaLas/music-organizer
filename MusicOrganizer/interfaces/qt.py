from PyQt4 import QtGui, QtCore;
from . import interface;
from .. import utils as utils;
import os;
import sys;
import platform;
import time;
import random;
from collections import deque;

#
# Copyright (c) by Patryk Jaworski
# Contact:
# -> E-mail: Patryk Jaworski <skorpion9312@gmail.com>
# -> XMPP/Jabber: skorpion9312@jabber.org
#

class Organizer(QtGui.QMainWindow, interface.Interface):
	__app = None;
	__statusBar = None;
	__menuBar = None;
	__path = None;
	__target = None;
	__badCharacters = None;
	__recursive = None;
	__copy = None;
	__delete = None;
	__deleteEmpty = None;
	__follow = None;
	__force = None;
	__scheme = None;
	__recognizeCovers = None;
	__normalizeTags = None;
	__numOk = 0;
	__numSkipped = 0;
	__numDeleted = 0;
	__numLeft = 0
	__toRemove = [];
	__numUntagged = 0
	__files = [];
	__progress = None;
	__duplicates = None;
	__dStrategy = None;
	__dAction = None;

	def __init__(self, args):
		self.__app = QtGui.QApplication(args);
		QtGui.QMainWindow.__init__(self);
		utils.ENABLE_VERBOSE = True;
		utils.init();
		self.__initUI();
	
	def operate(self):
		self.show();
		sys.exit(self.__app.exec_());

	# TODO: Add 'detect duplicates option'
	def __initUI(self):
		utils.verbose(_('Initializing UI...'));
		self.setWindowTitle('Music Organizer');
		self.resize(500, 300);
		self.setWindowIcon(QtGui.QIcon('./data/icons/icon.png'));
		self.__statusBar = self.statusBar();
		self.__menuBar = self.menuBar();

		# Toolbar
		start = QtGui.QAction(QtGui.QIcon('./data/icons/start.png'), 'Start', self);
		start.setStatusTip(_('Start organize'));
		self.connect(start, QtCore.SIGNAL('triggered()'), self.__startOrganize);
		exit = QtGui.QAction(QtGui.QIcon('./data/icons/exit.png'), 'Exit', self);
		exit.setStatusTip(_('Exit Music Organizer'));
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'));
		toolbar = self.addToolBar(_('Start'));
		toolbar.addAction(start);
		toolbar = self.addToolBar(_('Exit'));
		toolbar.addAction(exit);

		# Menubar
		tmp = self.__menuBar.addMenu(_('&File'));
		tmp.addAction(start);
		tmp.addAction(exit);
		tmp = self.__menuBar.addMenu(_('&Help'));
		about = QtGui.QAction(QtGui.QIcon('./data/icons/about.png'), 'About', self);
		about.connect(about, QtCore.SIGNAL('triggered()'), self.__about);
		tmp.addAction(about);

		# Main content
		container = QtGui.QWidget();
		vbox = QtGui.QVBoxLayout();
		topGrid = QtGui.QGridLayout();
		bottomGrid = QtGui.QGridLayout();
		self.__path = QtGui.QLineEdit();
		self.__path.setText(utils.getHomeDir());
		self.__target = QtGui.QLineEdit();
		self.__scheme = QtGui.QLineEdit();
		self.__scheme.setToolTip('Available blocks: {artist} {album} {date} {title} {old-file-name} {genre} {track}');
		self.__scheme.setStatusTip('Available blocks: {artist} {album} {date} {title} {old-file-name} {genre} {track}');
		self.__setDefaultScheme();
		self.__badCharacters = QtGui.QLineEdit();
		self.__badCharacters.setToolTip(_('This characters is used if "Normalize tags" is checked.'));
		self.__badCharacters.setStatusTip(_('This characters is used if "Normalize tags" is checked.'));
		self.__setDefaultBadCharacters();
		self.__replace = QtGui.QLineEdit();
		self.__replace.setToolTip(_('Replacement for any character from "Bad characters". Leave empty if you want to remove all bad characters.'));
		self.__replace.setStatusTip(_('Replacement for any character from "Bad characters". Leave empty if you want to remove all bad characters.'));
		b1 = QtGui.QPushButton(_('Browse'));
		b1.setStatusTip(_('Select search directory'));
		b2 = QtGui.QPushButton(_('Browse'));
		b2.setStatusTip(_('Select target directory'));
		b3 = QtGui.QPushButton(_('Set default'));
		b4 = QtGui.QPushButton(_('Set default'));
		self.connect(b1, QtCore.SIGNAL('clicked()'), self.__browsePath);
		self.connect(b2, QtCore.SIGNAL('clicked()'), self.__browseTarget);
		self.connect(b3, QtCore.SIGNAL('clicked()'), self.__setDefaultScheme);
		self.connect(b4, QtCore.SIGNAL('clicked()'), self.__setDefaultBadCharacters);

		self.__recursive = QtGui.QCheckBox(_('Recursive mode'));	
		self.__recursive.setStatusTip(_('Enable recursive mode'));
		self.__delete = QtGui.QCheckBox(_('Delete mode'));
		self.__delete.setStatusTip(_('Delete filtered directories'));
		self.__deleteEmpty = QtGui.QCheckBox(_('Clean directories'));
		self.__deleteEmpty.setStatusTip(_('Remove all empty directories'));
		self.__force = QtGui.QCheckBox(_('Force'));
		self.__force.setStatusTip(_('Force delete filtered directories'));
		self.__copy = QtGui.QCheckBox(_('Copy'));
		self.__copy.setStatusTip(_('Copy files instead of move'));
		self.__follow = QtGui.QCheckBox(_('Follow symlinks'));
		self.__follow.setStatusTip(_('Follow symlinks/links/shortcuts'));
		self.__normalizeTags = QtGui.QCheckBox(_('Normalize tags'));
		self.__normalizeTags.setStatusTip(_('Remove specified bad characters from tags (~,/,@,# etc.)'));
		self.__recognizeCovers = QtGui.QCheckBox(_('Recognize covers'));
		self.__recognizeCovers.setStatusTip('[NOT IMPLEMENTED YET] Try to recognize covers');
		self.__recognizeCovers.setDisabled(True);

		topGrid.setSpacing(10);
		topGrid.addWidget(QtGui.QLabel(_('Search path:')), 1, 0, QtCore.Qt.AlignRight);
		topGrid.addWidget(self.__path, 1, 1);
		topGrid.addWidget(b1, 1, 2);
		topGrid.addWidget(QtGui.QLabel(_('Target path:')), 2, 0, QtCore.Qt.AlignRight);
		topGrid.addWidget(self.__target, 2, 1);
		topGrid.addWidget(b2, 2, 2);
		topGrid.addWidget(QtGui.QLabel(_('Scheme:')), 3, 0, QtCore.Qt.AlignRight);
		topGrid.addWidget(self.__scheme, 3, 1);
		topGrid.addWidget(b3, 3, 2);
		topGrid.addWidget(QtGui.QLabel(_('Bad characters:')), 4, 0, QtCore.Qt.AlignRight);
		topGrid.addWidget(self.__badCharacters, 4, 1);
		topGrid.addWidget(b4, 4, 2);
		topGrid.addWidget(QtGui.QLabel(_('Replacement: ')), 5, 0, QtCore.Qt.AlignRight);
		topGrid.addWidget(self.__replace, 5, 1);

		bottomGrid.addWidget(self.__recursive, 1, 0);
		bottomGrid.addWidget(self.__follow, 1, 1);
		bottomGrid.addWidget(self.__copy, 1, 2);
		bottomGrid.addWidget(self.__delete, 2, 0);
		bottomGrid.addWidget(self.__force, 2, 1);
		bottomGrid.addWidget(self.__deleteEmpty, 2, 2);
		bottomGrid.addWidget(self.__normalizeTags, 3, 0);
		bottomGrid.addWidget(self.__recognizeCovers, 3, 1);

		duplicatesGrid = QtGui.QGridLayout();

		self.__dStrategy = QtGui.QComboBox();
		self.__dStrategy.addItem('MD5');
		self.__dStrategy.addItem('SHA1');
		self.__dStrategy.addItem(_('File name'));

		self.__dAction = QtGui.QComboBox();
		self.__dAction.addItem(_('Remove'));
		self.__dAction.addItem(_('Separate'));
		self.__dAction.addItem(_('Leave'));

		duplicatesGrid.addWidget(QtGui.QLabel(_('Strategy:')), 1, 0, QtCore.Qt.AlignRight);	
		duplicatesGrid.addWidget(self.__dStrategy, 1, 1);
		duplicatesGrid.addWidget(QtGui.QLabel(_('Action:')), 2, 0, QtCore.Qt.AlignRight);
		duplicatesGrid.addWidget(self.__dAction, 2, 1);
		duplicatesGrid.setColumnStretch(1, 2);

		self.__duplicates = QtGui.QGroupBox(_('Detect duplicates'));
		self.__duplicates.setLayout(duplicatesGrid);
		self.__duplicates.setStatusTip(_('[NOT IMPLEMENTED YET]'));
		self.__duplicates.setDisabled(True);

		topGroup = QtGui.QGroupBox(_('Main settings'));
		bottomGroup = QtGui.QGroupBox(_('Options'));
		topGroup.setLayout(topGrid);
		bottomGroup.setLayout(bottomGrid);
		vbox.addWidget(topGroup);
		vbox.addWidget(bottomGroup);
		vbox.addWidget(self.__duplicates);
		container.setLayout(vbox);
		self.setCentralWidget(container);
		
	def __browseTarget(self):
		target = self.__chooseDir(_('Select target directory'));
		if target:
			self.__target.setText(target);
	
	def __setDefaultScheme(self):
		self.__scheme.setText('{artist}{0}{album}{0}{title}'.replace('{0}', utils.DIR_SEPARATOR));
	
	def __setDefaultBadCharacters(self):
		self.__badCharacters.setText(utils.BAD_CHARS);

	def __browsePath(self):
		path = self.__chooseDir(_('Select search directory'));
		if path:
			self.__path.setText(path);

	def __chooseDir(self, msg):
		return QtGui.QFileDialog.getExistingDirectory(self, msg, utils.getHomeDir());

	def __clean(self):
		self.__numOk = 0;
		self.__numSkipped = 0;
		self.__numLeft = 0
		self.__numDeleted = 0;
		self.__numUntagged = 0
		self.__files = [];
		self.__toRemove = [];
	
	def __startOrganize(self):
		if self.__progress != None:
			self.__critical(_('Another hardcore organizing action is running now!'));
			return False;
		self.__clean();
		try:
			utils.prepare(self.__path.text(), self.__target.text());
			if self.__path.text()[-1] != utils.DIR_SEPARATOR:
				self.__path.insert(utils.DIR_SEPARATOR);
			if self.__target.text()[-1] != utils.DIR_SEPARATOR:
				self.__target.insert(utils.DIR_SEPARATOR);
		except Exception as e:
			self.__critical(str(e));
			return False;
		utils.verbose(_('Staring hardcore organizing action!'));
		self.__progress = QtGui.QProgressDialog('Initializing...', 'Cancel', 0, 100, self);
		self.__progress.setMinimumDuration(1);
		self.__progress.setAutoClose(False);
		self.__progress.setAutoReset(False);
		self.__progress.forceShow();
		self.__progress.open();
		self.__progress.setValue(0);
		queue = deque([self.__path.text()]);
		try:	
			while len(queue) != 0:
				if self.__progress.wasCanceled():
					raise KeyboardInterrupt(_('Canceled'));
				path = queue.popleft();
				try:
					files = os.listdir(path);
					if len(files) == 0:
						if self.__deleteEmpty.isChecked():
							self.__remove(path);
						else:
							utils.verbose(_('Skipping empty directory %s') % path);
						continue;
				except OSError:
					utils.verbose(_('Unable to list directory %s') % path);
					continue;
				lastTag = None;
				for f in files:
					if self.__progress.wasCanceled():
						raise KeyboardInterrupt(_('Canceled'));
					if os.path.islink(path + f) and not self.__follow.isChecked():
						utils.verbose(_('Skipping link %s...') % (path + f))
						continue;
					if os.path.isdir(path + f) and self.__recursive.isChecked():
						queue.append(path + f + utils.DIR_SEPARATOR);
						if self.__delete.isChecked() and path not in self.__toRemove:
							self.__toRemove.append(path);
						continue;
					if f[-4:].lower() == '.mp3':
						print(_('[I] Adding %s') % (path + f));
						if self.__delete.isChecked() and path not in self.__toRemove:
							self.__toRemove.append(path);
						self.__files.append(path + f);
						self.__progress.setLabelText(_('Preparing files (%d)') % len(self.__files));
						newMax = 0.9 if random.choice((0, 1, 2)) == 1 else 0.7;
						if len(self.__files) > self.__progress.maximum() * newMax:
							self.__progress.setMaximum(int(len(self.__files)) * 2);
						self.__progress.setValue(len(self.__files));
		except KeyboardInterrupt:
			return False;
		utils.verbose("Got %d files..." % len(self.__files));
		self.__numLeft = len(self.__files);
		self.__progress.setMaximum(self.__numLeft);
		if self.__numLeft != 0:
			self.__progress.setValue(0);
			self.__progress.setLabelText(_('Organizing files...'));
		else:
			self.__progress.setValue(self.__progress.maximum);
			self.__progress.setLabelText(_('No music files found!'));
			return True;
		try:
			for F in self.__files:
				if self.__progress.wasCanceled():
					raise KeyboardInterrupt();
				D = os.path.dirname(F);
				tag = utils.getTag(F);
				if not tag:
					self.__numUntagged += 1;
					tag = utils.getDefaultTag(F);
				print(tag);
				if self.__normalizeTags.isChecked():
					utils.BAD_CHARS = self.__badCharacters.text();
					utils.REPLACE_WITH = self.__replace.text();
					tag = utils.normalizeTags(tag);
				if utils.moveTrack(F, tag, self.__target.text(), self.__scheme.text(), self.__copy.isChecked()):
					self.__numOk += 1;
				else:
					self.__numSkipped += 1;
				self.__numLeft -= 1;

				self.__progress.setValue(self.__progress.value() + 1);
				self.__updateProgressLabel();
			try:
				print(self.__toRemove);
				while True:
					R = self.__toRemove.pop();
					self.__remove(R);
					self.__updateProgressLabel();
			except IndexError:
				pass;
		except KeyboardInterrupt:
			return False;
		self.__progress.setCancelButtonText(_('Ok'));
		self.__progress = None;
		return True;

	def __updateProgressLabel(self, label = None):
		if not label:
			info = ((_('Total'), len(self.__files)), (_('Left'), self.__numLeft), (_('Copied') if self.__copy.isChecked() else _('Moved'), self.__numOk), (_('Skipped'), self.__numSkipped), (_('Removed'), self.__numDeleted), (_('Untagged'), self.__numUntagged));
			label = '';
			for pair in info:
				label += '<p align="center">%s: <b>%d</b></p>' % (pair[0], pair[1]);
		self.__progress.setLabelText(label);

	def __remove(self, path):
		try:
			utils.verbose(_('Removing %s') % path);
			os.rmdir(path);
			self.__numDeleted += 1;
			return True;
		except Exception:
			utils.verbose(_('I can\'t remove  %s') % path);
			try:
				if self.__force.isChecked():
					print(_('Force remove...'));
					if self.__path.text() == self.__target.text() and path == self.__path:
						print('[W] %s' % 'Remove: skipping %s' % path);
						return False;
					utils.verbose(_('Force removing %s') % path);
					os.removedirs(path);
					self.__numDeleted += 1;
					return True;
				else:
					raise Exception();
			except:
				print('[W] %s' % _('Unable to remove directory %s...') % path);
		return False;

	def __critical(self, msg):
		QtGui.QMessageBox.critical(self, 'Music Organizer :: %s' % _('Critical error'), msg, QtGui.QMessageBox.Ok);

	def __about(self):
		QtGui.QMessageBox.about(self, 'Music Organizer :: %s' % ('About'),
		"""<b>Music Organizer</b> v{0}
		<p>Copyright &copy; by Patryk Jaworski &lt;skorpion9312@gmail.com&gt;</p>
		<p>{5}</p>
		<p>Python {1} - Qt {2} - PyQt {3} on {4}</p>""".format(utils.getVersion(), platform.python_version(), QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR, platform.system(), _('Automatically organize your MP3 music collection')));

