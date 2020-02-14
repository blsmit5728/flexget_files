#!/usr/bin/python 
import sys
import os
import logging, logging.handlers
import subprocess
from rarfile import RarFile
import time

#from pushbullet import Pushbullet
#ff = open('/home/bsmith/repos/flexget_files/bin/pb.key','r')
#l = ff.readline()
#key = l.rstrip()
#pb = Pushbullet(key)


LOG_FILE='/home/bsmith/logs/tor_comp/torrent_complete.log'
DOWNLOAD_PATH='/mnt/disk1/Downloads/completed'
STAGING_PATH='/mnt/disk1/Downloads/staging'
# If you're using a local checkout of Flexget, use flexget_vanilla.
# Otherwise use the one in your system
FLEXGET_COMMAND='flexget --loglevel debug --logfile /home/bsmith/logs/flexget/flexget-sorting.log --debug'
FLEXGET_SORTING_CONFIG='-c /home/bsmith/.flexget/sort.yml'
FLEXGET_TASK_PREFIX='Sort_Unpacked_'

FLEXGET_PATH_TASK={
    '/Movies/': 'Movies',
    '/TvShows/': 'TV_Shows',
    }

log = logging.getLogger("torrent_complete")
log.setLevel(logging.DEBUG)
logformat = logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s")

logfile = logging.FileHandler(LOG_FILE)
logfile.setFormatter(logformat)
logfile.setLevel(logging.INFO)
log.addHandler(logfile)

# Log to stdout and increase logging level if run from a console
if os.isatty(sys.stdin.fileno()):
    ch = logging.StreamHandler()
    ch.setFormatter(logformat)
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    FLEXGET_COMMAND += ' --debug'

if "/mnt/disk1/Library/" in sys.argv[3]:
    log.info('NOT Processing %s, file does not need to be unpacked' % sys.argv[2])
    sys.exit(0)

if len(sys.argv) != 4:
    log.error('%s called with %d arguments, it requires 3.' % (sys.argv[0],(len(sys.argv)-1)))
    str_called = ""
    for x in range(0,len(sys.argv)):
        str_called = str_called + str(sys.argv[x]) + " "
    log.error('args: %s' % str_called)
    sys.exit(-1)

torrent_id=sys.argv[1]
torrent_name=sys.argv[2]
torrent_path=sys.argv[3]
torrent_path=torrent_path+'/'


if "Movies" in torrent_path:
    sleep_time = 60
else:
    sleep_time = 30


log.debug('Sleeping %d seconds to allow for copy time...' % sleep_time)
time.sleep(sleep_time)
log.debug("%s called with torrent_id='%s', torrent_name='%s', torrent_path='%s'." % (sys.argv[0],
    torrent_id, torrent_name, torrent_path))

log.debug("RECALL: '%s %s %s %s'" % (sys.argv[0],torrent_id, torrent_name, torrent_path))

fd = open('/home/bsmith/logs/tor_comp/deluge_call.log','a')
s = sys.argv[0] + " " + torrent_id + " " + torrent_name + " " + torrent_path
fd.write(s)
fd.close()

if DOWNLOAD_PATH not in torrent_path:
    log.debug("Torrent '%s' path (%s) not in %s, skipping unrar" % (torrent_name,torrent_path,DOWNLOAD_PATH))

unrar_success = False

strings = ("Sample", "sample", "subs", "Subs", "Proof")

for path, task in FLEXGET_PATH_TASK.items():
    if DOWNLOAD_PATH+path in torrent_path:
        log.info('Processing %s as part of task %s.' % (torrent_name,task))
        for root, dirs, files in os.walk(torrent_path+'/'+torrent_name, topdown=False):
            #if "Sample" not in root and "Subs" not in root:
            if any(s in root for s in strings):
                log.debug('Not real directory: %s' % root)
            else:
                log.info('root=%s dirs=%s files=%s' % (root,dirs,files))
                #cmd='find "'+root+'" -type f -regex ".*\.\(\part[0-9]+\.\)?r\([0-9]+\|ar\)$" | head -1'
                cmd='find "'+root+'" -type f -regex ".*\.\(\part[0-9]+\.\)?r\([0-9]+\|ar\)$" | grep "\.rar" | grep -v "Subs"'
                log.debug('Shelling out: %s' % cmd)
                try:
                    ret = subprocess.check_output(cmd, shell=True)
                except subprocess.CalledProcessError:
                    log.error('Error on Find with: %s' % ret)
                    #str_err = "Error on Find command, rerun" + torrent_name
                    #push = pb.push_note("[Tor Complete]",str_err)
                    sys.exit(-2)
                ret = ret.rstrip()
                log.debug('Find Returned : %s' % ret)
                #cmd = 'mkdir "'+STAGING_PATH+path+torrent_id+'/" && cd "'+STAGING_PATH+path+torrent_id+'/" && easy_extract --force '+root                
                #log.debug('Shelling out  : %s' % cmd)
                #ret = subprocess.call(cmd, shell=True)
                # THIS IS THE RARFILE method
                rar_file = ret
                out_path = STAGING_PATH+path+torrent_id+'/'
                log.debug('file=%s dest=%s' % (rar_file,out_path))
                rf = RarFile(rar_file)
                try:
                    rf.extractall(path=out_path)
                    unrar_success = True
                except:
                    e = sys.exc_info()[0]
                    log.error("Error on Extraction with %s" % e)
                    #str_err = "Error on Extraction, error: " + e
                    #push = pb.push_note("[Tor Complete]",str_err)
                    sys.exit(-2)
                #with RarFile(rar_file,path=out_path) as rf:
                #    rf.extractall()
                #cmd='/home/bsmith/src/unrar/unrar x -o+ "'+ret+'" "'+STAGING_PATH+path+torrent_id+'/"' 
                #log.debug('Shelling out  : %s' % cmd)
                #ret = subprocess.call(cmd, shell=True)
                #if ret != 0:
                #    log.warning('Unrar command returned non-zero value %d.' % ret)
                #    sys.exit(-1)
                #else:
                #    unrar_success = True
        if unrar_success == True:
            cmd='find "'+STAGING_PATH+path+torrent_id+'" -type f -print0 | xargs -0 du -b | sort -nr | head -1'
            try:
                log.debug('Shelling out: %s' % cmd)
                # check_ouptut is not available in python 2.6
                main_file_size, main_file = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].split()
                main_file_size = int(main_file_size)
                cmd = 'du -b "'+STAGING_PATH+path+torrent_id+'"'
                log.debug('Shelling out: %s' % cmd)
                # check_ouptut is not available in python 2.6
                #total_size = int(subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True).communicate()[0].split()[0])
                total_size = int(subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].split()[0])
                log.debug('Total size: %d' % total_size)
                if main_file_size > (total_size * 0.9):
                    new_name = os.path.join(os.path.dirname(main_file), torrent_name+'.'+main_file.split('.')[-1])
                    log.debug('Names: %s,%s,%s' % (main_file, torrent_name, new_name));
                    log.debug('Renaming %s to %s because it is >90%% of the unpacked torrent'%(os.path.basename(main_file),  os.path.basename(new_name)))
                    os.rename(main_file, new_name)
                else:
                    log.warning('Couldn\'t find any files that were >90% of the unpacked torrent')
            except:
                log.error('Failed attempting to rename the main unpacked file: %s' % sys.exc_info()[0])
                raise   

            #cmd=FLEXGET_COMMAND+' '+FLEXGET_SORTING_CONFIG+' execute --task '+FLEXGET_TASK_PREFIX + task + (' --disable-advancement' if 'tv' in path else '')
            cmd='flexget --logfile /home/bsmith/.flexget/flexget-sorting.log -c /home/bsmith/.flexget/sort.yml execute --task ' + FLEXGET_TASK_PREFIX + task + (' --disable-advancement' if 'tv' in path else '')
            log.debug('Shelling out: %s' % cmd)
            ret = subprocess.call(cmd, shell=True)
            if ret != 0:
                log.warning('Flexget command returned non-zero value %d.' % ret)
            else:
                log.info("SUCCESS! %d\n" % ret)
        else:
            log.debug("Unrar Failed, or True never set")
    else:
        log.debug("Path %s not in %s" % (DOWNLOAD_PATH+path, torrent_path))

