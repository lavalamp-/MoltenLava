# -*- coding: utf-8 -*-
'''
@author: lavalamp

    Copyright 2014
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''
import logging
from time import sleep
from lib import LavaLib
from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


def scan_host(target_host, num_tries):
    nm = NmapProcess(target_host, options='-sT -Pn -T3')
    cur_try = 0
    while cur_try < num_tries:
        logger.debug(
            "Now running scan attempt #%d for host at %s."
            % (cur_try + 1, target_host)
        )
        result = nm.run_background()
        while nm.is_running():
            logger.debug(
                "Scan running. ETC: %s. DONE: %s."
                % (nm.etc, nm.progress)
            )
            sleep(2)
        if nm.rc != 0:
            logger.warning(
                "Scan #%d for host at %s failed!"
                % (cur_try + 1, target_host)
            )
            cur_try += 1
        else:
            logger.debug(
                "Scan for host at %s succeeded!"
                % (target_host,)
            )
            break
    if str(nm.state) != str(nm.DONE):
        logger.warning(
            "Scan for host at %s failed!"
            % (target_host,)
        )
        return
    else:
        try:
            parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            logger.error(
                "NmapParserException thrown: %s."
                % (e.msg,)
            )
        host = parsed.hosts[0]
        to_return = []
        for service in host.services:
            to_return.append(
                "%s//%s//%s//%s"
                % (
                    host.ipv4,
                    service.protocol,
                    str(service.port),
                    service.state
                )
            )
        return to_return


def main():
    print_greeting()
    LavaLib.configure_logging(logger)
    hosts_file_path = "target_hosts.txt"
    output_file = "scan_output.txt"
    start_time = datetime.now()
    with open(output_file, 'w+') as f:
        pass  # Clear file if it exists
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    logger.debug(
        "Getting hosts list out of file at %s."
        % hosts_file_path
    )
    with open(hosts_file_path, 'r') as f:
        c_split = [x.strip() for x in f.read().strip().split("\n")]
    logger.debug(
        "Total of %d hosts found in file at %s."
        % (len(c_split), hosts_file_path)
    )
    for cur_host in c_split:
        scan_host(cur_host, 1)  # First time is garbage
        results = scan_host(cur_host, 1)  # Second time's the charm!
        if results:
            with open(output_file, 'a') as f:
                for cur_result in results:
                    f.write(cur_result + "\n")
            logger.info(
                "Successfully wrote results for host at %s to file '%s'."
                % (cur_host, output_file)
            )
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


def print_greeting():
    print(LavaLib.LavaUIFactory.get_colorized_lavalamp_splash())
    print("                         /***************************\                             ")
    print("-= Presents the \033[31mLavaForeScoutScanner\033[0m, because F ForeScout =-")
    print("                         \***************************/                             ")
    print("")

logger = logging.getLogger("LavaContentDiscovery")

if __name__ == '__main__':
    main()
