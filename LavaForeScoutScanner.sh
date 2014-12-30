#!/bin/bash

get_number_of_scan_screen_sessions() {
	screen -ls | grep scan | wc -l | tr -d ' '
}

get_time_string() {
	date +"%m/%d %H:%M:%S"
}

run_scan_for_host() {
	screen -dmS $1.scan bash -c "nmap -sT -Pn -T3 $1; nmap -sT -Pn -T3 -oG $1.gnmap $1; cat $1.gnmap | grep \"Host: $1\" >> $2; rm $1.gnmap; bash;"
	# echo "screen -dmS $1.scan bash -c \"nmap -sT -Pn -T3 $1; nmap -sT -Pn -T3 -oG $1.gnmap $1; cat $1.gnmap | grep \"Host: $1\" >> $2; rm $1.gnmap;\""
	# echo "screen -S $1.scan nmap -sT -Pn -T3 $1; nmap -sT -Pn -T3 -oG $1.gnmap $1; cat $1.gnmap | grep \"Host: $1\" >> $2; rm $1.gnmap; bash;"
}

log_warn() {
	local TIME=$(get_time_string)
	echo -e "[$TIME] [\033[33m W \033[0m] $1" 1>&2
}

log_error() {
	local TIME=$(get_time_string)
	echo -e "[$TIME] [\033[91m E \033[0m] $1" 1>&2
}

log_info() {
	local TIME=$(get_time_string)
	echo -e "[$TIME] [\033[92m I \033[0m] $1" 1>&2
}

validate_arguments() {
	if [[ $# != 3 ]]; then
		log_warn "Illegal number of parameters passed to LavaForeScoutScanner.sh!"
		echo -1
	elif [[ ! -f $1 ]]; then
		log_warn "No file found at path '$1'!"
		echo -1
	elif [[ $(file --mime-type -b $1) != "text/plain" ]]; then
		log_warn "The file at '$1' does not appear to be a text file."
		echo -1
	elif [[ -f $2 ]]; then
		log_warn "File already exists at path '$2'! Please specify a path where a file does not already exist."
		echo -1
	elif [[ ! $3 =~ ^-?[0-9]+$ ]]; then
		log_warn "The value of '$2' is not an integer."
		echo -1
	else
		log_info "Arguments to LavaForeScoutScanner.sh validated. Input path: '$1' Number of processes: $2."
		echo 1
	fi
}

scan_from_file() {
	INPUT_FILE=$1
	OUTPUT_FILE=$2
	MAX_SCREEN_SESSIONS=$3
	log_info "Starting scan process from file at path '$1'."
	NUM_LINES=$(cat $1 | wc -l | tr -d ' ')
	log_info "Total number of lines in file at path '$1' is $NUM_LINES."
	while read CUR_LINE; do
		NUM_SESSIONS=$(get_number_of_scan_screen_sessions)
		if [ $NUM_SESSIONS -ge $MAX_SCREEN_SESSIONS ]; then
			log_info "Total of $NUM_SESSIONS screen sessions already running. Sleeping for 15 seconds."
			sleep 15
		else
			log_info "Kicking off scan for host at $CUR_LINE."
			run_scan_for_host $CUR_LINE $OUTPUT_FILE
		fi
	done < $1
	log_info "All hosts in file at path '$1' successfully scanned! Exiting."
}

main() {
	local ARG_CHECK=$(validate_arguments $@)
	if [[ $ARG_CHECK == -1 ]]; then
		log_error "Arguments passed to LavaForeScoutScanner failed to validate."
		log_error "Please review the script usage, change the arguments, and try again."
	else
		scan_from_file $@
	fi
}

#TODO Add usage
#TODO Add lavalamp splash
# Usage currently: bash LavaForeScoutScanner.sh <input host file> <output file> <max # of concurrent host scans>

main $@
