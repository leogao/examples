#!/bin/bash
# Option Description:
# -------------------
#
# Option description is based on getopts bash builtin. The description adds 
# a variable name feature to be used on future checks for required or optional
# values. The option description adds "=>VARIABLE_NAME" string. Variable name
# should be UPPERCASE. Valid characters are [A-Z_]*.
#
# A option description example:
#   OPT_DESC="a:=>A_VARIABLE|b:=>B_VARIABLE|c=>C_VARIABLE"
#
# -a option will require a value (the colon means that) and should be saved in
#    variable A_VARIABLE.
# "|" is used to separate options description.
# -b option rule applies the same as -a.
# -c option doesn't require a value (the colon absense means that) and its 
#    existence should be set in C_VARIABLE
#
#   ~$ echo get_options ${OPT_DESC}
#   a:b:c
#   ~$
#
# simple example
# --------------------------------------------------
# while getopts a:bc flag; do
#   case $flag in
#     a)
#       echo "-a used: $OPTARG";
#       ;;
#     b)
#       echo "-b used";
#       ;;
#     c)
#       echo "-c used";
#       ;;
#     ?)
#       exit;
#       ;;
#   esac
# done
# 
# shift $(( OPTIND - 1 ));
# --------------------------------------------------
#
# Required options 
REQUIRED_DESC="a:=>REQ_A_VAR_VALUE|B:=>REQ_B_VAR_VALUE|c=>REQ_C_VAR_FLAG"

# Optional options (duh)
OPTIONAL_DESC="P:=>OPT_P_VAR_VALUE|r=>OPT_R_VAR_FLAG"

function usage {
    IFS="|"
    printf "%s" ${0}
    for i in ${REQUIRED_DESC};
    do
        VARNAME=$(echo $i | sed -e "s/.*=>//g")
        printf " %s" "-${i:0:1} $VARNAME"
    done

    for i in ${OPTIONAL_DESC};
    do
        VARNAME=$(echo $i | sed -e "s/.*=>//g")
        printf " %s" "[-${i:0:1} $VARNAME]"
    done
    printf "\n"
    unset IFS
    exit
}

# Auxiliary function that returns options characters to be passed
# into 'getopts' from a option description.
# Arguments:
#   $1: The options description (SEE TOP)
#
# Example:
#   OPT_DESC="h:=>H_VAR|f:=>F_VAR|P=>P_VAR|W=>W_VAR"
#   OPTIONS=$(get_options ${OPT_DESC})
#   echo "${OPTIONS}"
#
# Output:
#   "h:f:PW"

function get_options {
    echo ${1} | sed -e "s/\([a-zA-Z]\:\?\)=>[A-Z_]*|\?/\1/g"
}

# Auxiliary function that returns all variable names separated by '|'
# Arguments:
#       $1: The options description (SEE TOP)
#
# Example:
#       OPT_DESC="h:=>H_VAR|f:=>F_VAR|P=>P_VAR|W=>W_VAR"
#       VARNAMES=$(get_values ${OPT_DESC})
#       echo "${VARNAMES}"
#
# Output:
#       "H_VAR|F_VAR|P_VAR|W_VAR"

function get_variables {
    echo ${1} | sed -e "s/[a-zA-Z]\:\?=>\([^|]*\)/\1/g"
}

# Auxiliary function that returns the variable name based on the
# option passed by.
# Arguments:
#   $1: The options description (SEE TOP)
#   $2: The option which the variable name wants to be retrieved
#
# Example:
#   OPT_DESC="h:=>H_VAR|f:=>F_VAR|P=>P_VAR|W=>W_VAR"
#   H_VAR=$(get_variable_name ${OPT_DESC} "h")
#   echo "${H_VAR}"
#
# Output:
#   "H_VAR"

function get_variable_name {
    VAR=$(echo ${1} | sed -e "s/.*${2}\:\?=>\([^|]*\).*/\1/g")
    if [[ ${VAR} == ${1} ]]; then
        echo ""
    else
        echo ${VAR}
    fi
}

# Gets the required options from the required description
REQUIRED=$(get_options ${REQUIRED_DESC})

# Gets the optional options (duh) from the optional description
OPTIONAL=$(get_options ${OPTIONAL_DESC})

# or... $(get_options "${OPTIONAL_DESC}|${REQUIRED_DESC}")

# The colon at starts instructs getopts to remain silent

while getopts ":${REQUIRED}${OPTIONAL}" OPTION
do
    [[ ${OPTION} == ":" ]] && usage
    VAR=$(get_variable_name "${REQUIRED_DESC}|${OPTIONAL_DESC}" ${OPTION})
    [[ -n ${VAR} ]] && eval "$VAR=${OPTARG}"
done

shift $(($OPTIND - 1))

# Checks for required options. Report an error and exits if
# required options are missing.

# Using function version ...
VARS=$(get_variables ${REQUIRED_DESC})
IFS="|"
for VARNAME in $VARS;
do
    [[ -v ${VARNAME} ]] || usage
done
unset IFS

# ... or using IFS Version (no function)
OLDIFS=${IFS}
IFS="|"
for i in ${REQUIRED_DESC};
do
    VARNAME=$(echo $i | sed -e "s/.*=>//g")
    [[ -v ${VARNAME} ]] || usage
    echo $VARNAME
    printf "%s %s %s\n" "-${i:0:1}" "${!VARNAME:=present}" "${VARNAME}"
done
IFS=${OLDIFS}
