/*
 *  prjpeppercorn -- GateMate FPGAs Bitstream Documentation and Tools
 *
 *  Copyright (C) 2024  The Project Peppercorn Authors.
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */

#include <boost/program_options.hpp>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <streambuf>
#include "Bitstream.hpp"
#include "Chip.hpp"
#include "ChipConfig.hpp"
#include "version.hpp"

int main(int argc, char *argv[])
{
    using namespace GateMate;
    namespace po = boost::program_options;

    po::options_description options("Allowed options");
    options.add_options()("help,h", "show help");
    options.add_options()("verbose,v", "verbose output");
    options.add_options()("reset", "reset all configuration latches with CMD_CFGRST");
    options.add_options()("crcmode", po::value<std::string>(), "CRC error behaviour (check, ignore, unused)");
    options.add_options()("spimode", po::value<std::string>(), "SPI Mode to use (single, dual, quad)");
    options.add_options()("reconfig", "enable reconfiguration in bitstream");
    options.add_options()("background", "enable background reconfiguration in bitstream");
    options.add_options()("bootaddr", po::value<int>(), "boot address for secondary bitstream");
    po::positional_options_description pos;
    options.add_options()("input", po::value<std::string>()->required(), "input textual configuration");
    pos.add("input", 1);
    options.add_options()("bit", po::value<std::string>(), "output bitstream file");
    pos.add("bit", 1);

    po::variables_map vm;

    try {
        po::parsed_options parsed = po::command_line_parser(argc, argv).options(options).positional(pos).run();
        po::store(parsed, vm);
        po::notify(vm);
    } catch (po::required_option &e) {
        std::cerr << "Error: input file is mandatory." << std::endl << std::endl;
        goto help;
    } catch (std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl << std::endl;
        goto help;
    }

    if (vm.count("help")) {
    help:
        std::filesystem::path path(argv[0]);
        std::cerr << "Open Source Tools for GateMate FPGAs Version " << git_describe_str << std::endl;
        std::cerr << "Copyright (C) 2024 The Project Peppercorn Authors" << std::endl;
        std::cerr << std::endl;
        std::cerr << path.stem().c_str() << ": GateMate bitstream packer" << std::endl;
        std::cerr << std::endl;
        std::cerr << "Usage: " << argv[0] << " input.config [output.bit] [options]" << std::endl;
        std::cerr << std::endl;
        std::cerr << options << std::endl;
        return vm.count("help") ? 0 : 1;
    }

    std::ifstream config_file(vm["input"].as<std::string>());
    if (!config_file) {
        std::cerr << "Failed to open input file" << std::endl;
        return 1;
    }

    std::map<std::string, std::string> bitopts;

    if (vm.count("reset")) {
        bitopts["reset"] = "yes";
    }

    if (vm.count("crcmode")) {
        bitopts["crcmode"] = vm["crcmode"].as<std::string>();
    }

    if (vm.count("spimode")) {
        bitopts["spimode"] = vm["spimode"].as<std::string>();
    }

    if (vm.count("reconfig")) {
        bitopts["reconfig"] = "yes";
    }

    if (vm.count("background")) {
        bitopts["background"] = "yes";
    }

    if (vm.count("bootaddr")) {
        bitopts["bootaddr"] = std::to_string(vm["bootaddr"].as<int>());
    }

    std::string textcfg((std::istreambuf_iterator<char>(config_file)), std::istreambuf_iterator<char>());

    ChipConfig cc;
    try {
        cc = ChipConfig::from_string(textcfg);
    } catch (std::runtime_error &e) {
        std::cerr << "Failed to process input config: " << e.what() << std::endl;
        return 1;
    }

    Chip c = cc.to_chip();
    Bitstream b = Bitstream::serialise_chip(c, bitopts);
    if (vm.count("bit")) {
        std::ofstream bit_file(vm["bit"].as<std::string>(), std::ios::binary);
        if (!bit_file) {
            std::cerr << "Failed to open output file" << std::endl;
            return 1;
        }
        b.write_bit(bit_file);
    }
    return 0;
}
