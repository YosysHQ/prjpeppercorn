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

#include "ChipConfig.hpp"
#include <iomanip>
#include <iostream>
#include <sstream>
#include "Chip.hpp"
#include "TileBitDatabase.hpp"
#include "Util.hpp"

namespace GateMate {

std::string ChipConfig::to_string() const
{
    std::stringstream ss;
    ss << ".device " << chip_name << std::endl << std::endl;
    for (const auto &config : configs) {
        if (!config.second.empty()) {
            ss << ".config " << config.first << " " << std::endl;
            ss << config.second;
            ss << std::endl;
        }
    }
    for (const auto &ser : serdes) {
        if (!ser.second.empty()) {
            ss << ".serdes " << ser.first << " " << std::endl;
            ss << ser.second;
            ss << std::endl;
        }
    }
    for (const auto &tile : tiles) {
        if (!tile.second.empty()) {
            ss << ".tile " << tile.first.die << " " << tile.first.x << " " << tile.first.y << std::endl;
            ss << tile.second;
            ss << std::endl;
        }
    }
    for (const auto &bram : brams) {
        if (!bram.second.empty()) {
            ss << ".bram " << bram.first.die << " " << bram.first.x << " " << bram.first.y << std::endl;
            ss << bram.second;
            ss << std::endl;
        }
    }
    for (const auto &bram : bram_data) {
        if (!bram.second.empty()) {
            ss << ".bram_init " << bram.first.die << " " << bram.first.x << " " << bram.first.y << std::endl;
            std::ios_base::fmtflags f(ss.flags());
            for (size_t i = 0; i < bram.second.size(); i++) {
                ss << std::setw(2) << std::setfill('0') << std::hex << (int)bram.second.at(i);
                if (i % 40 == 39)
                    ss << std::endl;
                else
                    ss << " ";
            }
            ss.flags(f);
            ss << std::endl;
        }
    }
    return ss.str();
}

ChipConfig ChipConfig::from_string(const std::string &config)
{
    std::stringstream ss(config);
    ChipConfig cc;
    while (!skip_check_eof(ss)) {
        std::string verb;
        ss >> verb;
        if (verb == ".device") {
            ss >> cc.chip_name;
        } else if (verb == ".config") {
            int die;
            ss >> die;
            TileConfig tc;
            ss >> tc;
            cc.configs.emplace(die, tc);
        } else if (verb == ".serdes") {
            int die;
            ss >> die;
            TileConfig tc;
            ss >> tc;
            cc.serdes.emplace(die, tc);
        } else if (verb == ".tile") {
            CfgLoc loc;
            ss >> loc.die;
            ss >> loc.x;
            ss >> loc.y;
            TileConfig tc;
            ss >> tc;
            cc.tiles.emplace(loc, tc);
        } else if (verb == ".bram") {
            CfgLoc loc;
            ss >> loc.die;
            ss >> loc.x;
            ss >> loc.y;
            TileConfig tc;
            ss >> tc;
            cc.brams.emplace(loc, tc);
        } else if (verb == ".bram_init") {
            CfgLoc loc;
            ss >> loc.die;
            ss >> loc.x;
            ss >> loc.y;
            std::ios_base::fmtflags f(ss.flags());
            while (!skip_check_eor(ss)) {
                uint16_t value;
                ss >> std::hex >> value;
                cc.bram_data[loc].push_back(value);
            }
            ss.flags(f);
        } else {
            throw std::runtime_error("unrecognised config entry " + verb);
        }
    }
    return cc;
}

Chip ChipConfig::to_chip() const
{
    Chip chip(chip_name);
    for (int d = 0; d < chip.get_max_die(); d++) {
        auto &die = chip.get_die(d);
        CfgLoc loc;
        loc.die = d;
        for (int y = 0; y < die.get_max_row(); y++) {
            loc.y = y;
            for (int x = 0; x < die.get_max_col(); x++) {
                loc.x = x;
                if (tiles.count(loc)) {
                    TileBitDatabase db(x, y);
                    const TileConfig &cfg = tiles.at(loc);
                    die.write_latch(x, y, db.config_to_data(cfg));
                }
            }
        }
        RamBitDatabase ram_db;
        for (int y = 0; y < die.get_max_ram_row(); y++) {
            loc.y = y;
            for (int x = 0; x < die.get_max_ram_col(); x++) {
                loc.x = x;
                if (brams.count(loc)) {
                    const TileConfig &cfg = brams.at(loc);
                    die.write_ram(x, y, ram_db.config_to_data(cfg));
                }
                if (bram_data.count(loc))
                    die.write_ram_data(x, y, bram_data.at(loc), 0);
            }
        }
        ConfigBitDatabase cfg_db;
        if (configs.count(d)) {
            const TileConfig &cfg = configs.at(d);
            die.write_die_cfg(cfg_db.config_to_data(cfg));
        }
        SerdesBitDatabase ser_db;
        if (serdes.count(d)) {
            const TileConfig &cfg = serdes.at(d);
            die.write_serdes_cfg(ser_db.config_to_data(cfg));
        }
    }

    return chip;
}

ChipConfig ChipConfig::from_chip(const Chip &chip)
{
    ChipConfig cc;
    cc.chip_name = chip.get_name();
    for (int d = 0; d < chip.get_max_die(); d++) {
        auto &die = chip.get_die(d);
        CfgLoc loc;
        loc.die = d;
        for (int y = 0; y < die.get_max_row(); y++) {
            loc.y = y;
            for (int x = 0; x < die.get_max_col(); x++) {
                loc.x = x;
                TileBitDatabase db(x, y);
                if (!die.is_latch_empty(x, y))
                    cc.tiles.emplace(loc, db.data_to_config(die.get_latch_config(x, y)));
            }
        }
        RamBitDatabase ram_db;
        for (int y = 0; y < die.get_max_ram_row(); y++) {
            loc.y = y;
            for (int x = 0; x < die.get_max_ram_col(); x++) {
                loc.x = x;
                if (!die.is_ram_empty(x, y)) {
                    cc.brams.emplace(loc, ram_db.data_to_config(die.get_ram_config(x, y)));
                    if (!die.is_ram_data_empty(x, y)) {
                        cc.bram_data.emplace(loc, die.get_ram_data(x, y));
                    }
                }
            }
        }
        ConfigBitDatabase cfg_db;
        cc.configs.emplace(d, cfg_db.data_to_config(die.get_die_config()));
        SerdesBitDatabase ser_db;
        cc.serdes.emplace(d, ser_db.data_to_config(die.get_serdes_config()));
    }
    return cc;
}

} // namespace GateMate
