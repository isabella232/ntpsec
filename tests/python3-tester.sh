#! /bin/sh
# keep this POSIX sh compatible.  No bash-isms!
# replace |& with 2>&1 |

# This is a clone of option-tester.sh
# to build with python3 and do minimal (version) testing.

if [ "`which python3 2>/dev/null`" = "" ]
then
  echo "# Error: No python3 on this system."
  exit 1
fi

# set pipefail to catch pipeline failures
# Unfortunately, it doesn't work on some older sh-es
if /bin/sh -c "set -o pipefail" 2> /dev/null
then
  set -o pipefail
fi

DISABLE_NTS=""
if pkg-config --version 2>/dev/null 1>/dev/null
then
  if ! pkg-config openssl --atleast-version=1.1.1
  then
    DISABLE_NTS="--disable-nts"
  fi
else
  if ! $PYTHON ../wafhelpers/openssl.py
  then
    DISABLE_NTS="--disable-nts"
  fi
fi

doit ()
{
  DIR=test-$1
  [ ! -d $DIR ] && mkdir $DIR
  rm -rf $DIR/*
  python3 ./waf configure $DISABLE_NTS --out=$DIR $2 2>&1 | tee    $DIR/test.log
  WAF1=$?
  WAF2=0
  WAF3=0
  if [ "$WAF1" = 0 ]
  then
  echo                            2>&1   | tee -a $DIR/test.log
  python3 ./waf build             2>&1   | tee -a $DIR/test.log
  WAF2=$?
  if [ "$WAF2" = 0 ]
  then
  echo                            2>&1   | tee -a $DIR/test.log
  python3 ./waf check             2>&1   | tee -a $DIR/test.log
  WAF3=$?
  fi
  fi
  if [ "$WAF1" != 0 -o "$WAF2" != 0 -o "$WAF3" != 0 ] 
  then
    echo                          2>&1   | tee -a $DIR/test.log
    echo "Trouble with $DIR"      2>&1   | tee -a $DIR/test.log
  fi
  echo
  echo
}

# Build with only one set of options.  The options don't change
# the Python side of things.

doit python3 "--disable-droproot --disable-mdns-registration --disable-manpage"


grep warning:                    test*/test.log
grep error:                      test*/test.log
grep "The configuration failed"  test*/test.log
grep ^Trouble                    test*/test.log
echo

echo -n "## ";  python3 --version
if test -n "$PYTHONPATH"
then
  echo "## PYTHONPATH is" \"$PYTHONPATH\"
fi

if ! /bin/sh -c "set -o pipefail" 2> /dev/null
then
  echo "### Old sh - no pipefail"
  echo "### We can't test for errors during build"
  echo "### You will have to scan the log files."
fi

