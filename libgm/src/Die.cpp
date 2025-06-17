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

#include "Die.hpp"
#include "Util.hpp"

namespace GateMate {

Die::Die()
{
    for (int y = 0; y < MAX_ROWS; y++) {
        for (int x = 0; x < MAX_COLS; x++) {
            latch[std::make_pair(x, y)] = std::vector<uint8_t>();
            latch[std::make_pair(x, y)].reserve(LATCH_BLOCK_SIZE);
        }
    }
    for (int y = 0; y < MAX_RAM_ROWS; y++) {
        for (int x = 0; x < MAX_RAM_COLS; x++) {
            ram[std::make_pair(x, y)] = std::vector<uint8_t>();
            ram[std::make_pair(x, y)].reserve(RAM_BLOCK_SIZE);
            ram_data[std::make_pair(x, y)] = std::vector<uint8_t>();
        }
    }
    serdes_cfg = std::vector<uint8_t>(SERDES_CFG_SIZE, 0x00);
    die_cfg = std::vector<uint8_t>(DIE_CONFIG_SIZE, 0x00);
}

bool Die::is_latch_empty(int x, int y) const { return latch.at(std::make_pair(x, y)).empty(); }

bool Die::is_cpe_empty(int x, int y) const
{
    auto &block = latch.at(std::make_pair(x, y));
    for (int i = 0; i < 40; i++)
        if (block[i] != 0x00)
            return false;
    return true;
}

bool Die::is_ram_empty(int x, int y) const { return ram.at(std::make_pair(x, y)).empty(); }

bool Die::is_ram_data_empty(int x, int y) const { return ram_data.at(std::make_pair(x, y)).empty(); }

bool Die::is_pll_cfg_empty(int index) const
{
    int pos = index * PLL_CFG_SIZE;
    for (int i = 0; i < PLL_CFG_SIZE; i++)
        if (die_cfg[i + pos] != 0x00)
            return false;
    return true;
}

bool Die::is_clkin_cfg_empty() const
{
    int pos = PLL_CFG_SIZE * MAX_PLL * 2;
    for (int i = 0; i < CLKIN_CFG_SIZE; i++)
        if (die_cfg[i + pos] != 0x00)
            return false;
    return true;
}

bool Die::is_glbout_cfg_empty() const
{
    int pos = PLL_CFG_SIZE * MAX_PLL * 2 + CLKIN_CFG_SIZE;
    for (int i = 0; i < GLBOUT_CFG_SIZE; i++)
        if (die_cfg[i + pos] != 0x00)
            return false;
    return true;
}

bool Die::is_status_cfg_empty() const
{
    int pos = STATUS_CFG_START;
    // First two bytes contain status change commands
    for (int i = 2; i < STATUS_CFG_SIZE; i++)
        if (die_cfg[i + pos] != 0x00)
            return false;
    return true;
}

bool Die::is_serdes_cfg_empty() const
{
    for (int i = 0; i < SERDES_CFG_SIZE; i++)
        if (serdes_cfg[i] != 0x00)
            return false;
    return true;
}

bool Die::is_using_cfg_gpios() const { return die_cfg[STATUS_CFG_START + 2] & 0x08; }

uint8_t Die::get_d2d_config() const { return die_cfg[DIE_CONFIG_SIZE - 1]; }

void Die::write_latch(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    auto &block = latch.at(std::make_pair(x, y));
    block.resize(LATCH_BLOCK_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

void Die::write_ff_init(int x, int y, uint8_t data)
{
    auto &block = latch.at(std::make_pair(x, y));
    block.resize(LATCH_BLOCK_SIZE, 0x00);
    block[LATCH_BLOCK_SIZE - 1] = data;
}

void Die::write_ram(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    auto &block = ram.at(std::make_pair(x, y));
    block.resize(RAM_BLOCK_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

void Die::write_ram_data(int x, int y, const std::vector<uint8_t> &data, uint16_t addr)
{
    int pos = addr;
    auto &block = ram_data.at(std::make_pair(x, y));
    block.resize(MEMORY_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

void Die::write_status(const std::vector<uint8_t> &data)
{
    int pos = STATUS_CFG_START;
    for (auto d : data)
        die_cfg[pos++] = d;
    // Clean command bits, we do not wish this exported
    pos = STATUS_CFG_START;
    die_cfg[pos++] = 0x00;
    die_cfg[pos++] = 0x00;
}

void Die::write_pll_select(uint8_t select, const std::vector<uint8_t> &data)
{
    for (int i = 0; i < MAX_PLL; i++) {
        if (select & (1 << i)) {
            int pos = i * 2 * PLL_CFG_SIZE;
            if (select & (1 << (i + 4))) {
                pos += PLL_CFG_SIZE;
            }
            for (size_t j = 0; j < PLL_CFG_SIZE; j++)
                die_cfg[pos++] = data[j];
        }
    }
    int pos = PLL_CFG_SIZE * MAX_PLL * 2; // start after PLL data;
    for (size_t j = PLL_CFG_SIZE; j < data.size(); j++)
        die_cfg[pos++] = data[j];
}

void Die::write_d2d_config(uint8_t data) { die_cfg[DIE_CONFIG_SIZE - 1] = data; }

} // namespace GateMate
