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
import glob
import re
import argparse
import json
from lib import LavaLib
from lxml import html
from datetime import datetime


class LavaEyeWitnessProcessor(object):

    _report_endpoints = None
    _report_files = None
    _error_count = 0

    def __init__(
            self,
            report_path,
            *args,
            **kwargs
            ):
        logger.debug(
            "LavaEyeWitnessProcessor instantiated with path of %s."
            % (report_path,)
        )
        if not report_path.endswith("/"):
            logger.warning(
                "Possible error - configured path does not end with '/'."
                " New path is %s."
                % (report_path + "/",)
            )
            report_path = report_path + "/"
        self._report_path = report_path

    def __get_endpoints_from_files(self):
        results = []
        for cur_file in self.report_files:
            logger.debug(
                "Now processing file at %s."
                % (cur_file,)
            )
            root_node = self.__get_root_node_from_file(cur_file)
            tr_nodes = root_node.xpath("//tr")
            before_count = len(results)
            for cur_node in tr_nodes[1:]:
                result = self.__process_tr_node(cur_node)
                if not result:
                    logger.warning("<tr> node processed but empty!")
                else:
                    results.append(result)
            after_count = len(results)
            logger.debug(
                "Total of %d endpoints found within file at %s."
                % (after_count - before_count, cur_file)
            )
        logger.debug(
            "All files have been processed. Total number of endpoints "
            "found was %d."
            % (len(results))
        )
        return results

    def __get_root_node_from_file(self, file_path):
        return html.parse(file_path).getroot()

    def __process_tr_node(self, tr_node):
        if not tr_node.xpath('td/div'):
            return None
        description = tr_node.xpath('td/div')[0].text_content()
        to_return = {}
        for cur_line in [x.strip() for x in description.split("\n")]:
            try:
                if not cur_line:
                    continue
                if re.match("^http(s)?://", cur_line):
                    to_return['target_url'] = cur_line
                if re.match("^Page Title:", cur_line):
                    title = re.match("^Page Title: (.*)$", cur_line).groups()[0]
                    to_return['page_title'] = title
                if re.match("^Server:", cur_line):
                    server = re.match("^Server: (.*)$", cur_line).groups()[0]
                    to_return['server'] = server
                if re.match("^Content-Type:", cur_line):
                    c_type = re.match("^Content-Type: (.*)$", cur_line).groups()[0]
                    to_return['content_type'] = c_type
                if re.match("^Content-Length:", cur_line):
                    c_length = re.match("^Content-Length: (.*)$", cur_line).groups()[0]
                    to_return['content_length'] = c_length
                if re.match("^X-Powered-By:", cur_line):
                    p_by = re.match("^X-Powered-By: (.*)$", cur_line).groups()[0]
                    to_return['powered_by'] = p_by
                if re.match("^Via:", cur_line):
                    via = re.match("^Via: (.*)$", cur_line).groups()[0]
                    to_return['via'] = via
                if re.match("^Set-Cookie:", cur_line):
                    cookies = re.match("^Set-Cookie: (.*)$", cur_line).groups()[0]
                    to_return['cookies'] = cookies
            except AttributeError as e:
                logger.error(
                    "AttributeError thrown! %s."
                    % (e.message)
                )
                self._error_count += 1
        logger.debug(
            "Fields discovered for <tr> node: %s."
            % (to_return.keys())
        )
        return to_return

    @property
    def report_endpoints(self):
        if not self._report_endpoints:
            self._report_endpoints = self.__get_endpoints_from_files()
            logger.info(
                "Total number of %d endpoints found associated with "
                "report at %s."
                % (len(self._report_endpoints), self.report_path)
            )
        return self._report_endpoints

    @property
    def report_files(self):
        if not self._report_files:
            self._report_files = glob.glob(self.report_path + "*.html")
            logger.debug(
                "Total number of %d HTML files found associated "
                "with report at %s."
                % (len(self._report_files), self.report_path,)
            )
        return self._report_files

    @property
    def report_path(self):
        return self._report_path


def main():
    print_greeting()
    args = parse_arguments()
    opts = vars(args)
    LavaLib.configure_logging(logger, args.log_level)
    start_time = datetime.now()
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    processor = LavaEyeWitnessProcessor(**opts)
    results = processor.report_endpoints
    logger.info(
        "Writing results to file at %s."
        % (args.output_path,)
    )
    with open(args.output_path, "w+") as f:
        f.write(json.dumps(results))
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="LavaEyewitnessProcessor - for processing "
                    "pesky EyeWitness reports"
    )
    parser.add_argument(
        "--log-level",
        required=False,
        help="The log message level to receive when running the script. Valid"
             "values are DEBUG, INFO, WARNING, ERROR, CRITICAL.",
        action="store",
        dest="log_level",
        metavar="<DEBUG|INFO|WARNING|ERROR|CRITICAL>",
        default="INFO",
        type=str
    )
    parser.add_argument(
        "--input-path",
        "-i",
        required=True,
        help="The path to the directory containing the "
             "EyeWitness report HTML files.",
        dest="report_path",
        action="store",
        type=str,
        metavar="/a/path/to/an/eyewitness/report/"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        help="The path where results of processing the EyeWitness "
             "report should be written. **WILL OVERWRITE EXISTING FILES**",
        dest="output_path",
        action="store",
        type=str,
        metavar="/a/path/to/store/the/output/to"
    )
    return parser.parse_args()


def print_greeting():
    print(LavaLib.LavaUIFactory.get_colorized_lavalamp_splash())
    print("                         /***************************\                             ")
    print("-= Presents the \033[31mLavaEyeWitnessProcessor\033[0m, for handling pesky EyeWitness reports =-")
    print("                         \***************************/                             ")
    print("")

logger = logging.getLogger("LavaEyeWitnessProcessor.py")

if __name__ == "__main__":
    main()
