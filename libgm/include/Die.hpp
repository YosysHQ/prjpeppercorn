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

#ifndef LIBGATEMATE_DIE_HPP
#define LIBGATEMATE_DIE_HPP

#include <cstdint>
#include <map>
#include <string>
#include <vector>

namespace GateMate {

class Die
{
  public:
    static constexpr int MAX_ROWS = 66;
    static constexpr int MAX_COLS = 82;
    static constexpr int MAX_RAM = 32;
    static constexpr int MAX_RAM_ROWS = 8;
    static constexpr int MAX_RAM_COLS = 4;
    static constexpr int LATCH_BLOCK_SIZE = 112 + 1; // Added one more byte for FF_INIT
    static constexpr int RAM_BLOCK_SIZE = 27;
    static constexpr int MEMORY_SIZE = 5120;
    static constexpr int MAX_PLL = 4;
    static constexpr int PLL_CFG_SIZE = 12;
    static constexpr int CLKIN_CFG_SIZE = 4;
    static constexpr int GLBOUT_CFG_SIZE = 8;
    static constexpr int STATUS_CFG_SIZE = 12;
    static constexpr int STATUS_CFG_START = PLL_CFG_SIZE * MAX_PLL * 2 + CLKIN_CFG_SIZE + GLBOUT_CFG_SIZE;
    static constexpr int DIE_CONFIG_SIZE = STATUS_CFG_START + STATUS_CFG_SIZE + 1;
    static constexpr int FF_INIT_RESET = 2;
    static constexpr int FF_INIT_SET = 3;
    static constexpr int SERDES_CFG_SIZE = 186;

  public:
    explicit Die();

    // Get max row and column
    int get_max_row() const { return MAX_ROWS; }
    int get_max_col() const { return MAX_COLS; }
    int get_max_ram_row() const { return MAX_RAM_ROWS; }
    int get_max_ram_col() const { return MAX_RAM_COLS; }

    bool is_latch_empty(int x, int y) const;
    bool is_cpe_empty(int x, int y) const;
    bool is_ram_empty(int x, int y) const;
    bool is_ram_data_empty(int x, int y) const;
    bool is_pll_cfg_empty(int index) const;
    bool is_clkin_cfg_empty() const;
    bool is_glbout_cfg_empty() const;
    bool is_status_cfg_empty() const;
    bool is_using_cfg_gpios() const;
    bool is_serdes_cfg_empty() const;
    uint8_t get_d2d_config() const;

    void write_latch(int x, int y, const std::vector<uint8_t> &data);
    void write_ram(int x, int y, const std::vector<uint8_t> &data);
    void write_ram_data(int x, int y, const std::vector<uint8_t> &data, uint16_t addr);
    void write_pll_select(uint8_t select, const std::vector<uint8_t> &data);
    void write_d2d_config(uint8_t data);
    void write_die_cfg(const std::vector<uint8_t> &data) { die_cfg = data; }
    void write_serdes_cfg(const std::vector<uint8_t> &data) { serdes_cfg = data; }
    void write_ff_init(int x, int y, uint8_t data);
    void write_status(const std::vector<uint8_t> &data);

    const std::vector<uint8_t> get_latch_config(int x, int y) const { return latch.at(std::make_pair(x, y)); }
    const std::vector<uint8_t> get_ram_config(int x, int y) const { return ram.at(std::make_pair(x, y)); }
    const std::vector<uint8_t> get_ram_data(int x, int y) const { return ram_data.at(std::make_pair(x, y)); }
    const std::vector<uint8_t> get_serdes_config() const { return serdes_cfg; }
    const std::vector<uint8_t> get_die_config() const { return die_cfg; }

  private:
    std::map<std::pair<int, int>, std::vector<uint8_t>> latch;    // Config latches
    std::map<std::pair<int, int>, std::vector<uint8_t>> ram;      // Config RAM
    std::map<std::pair<int, int>, std::vector<uint8_t>> ram_data; // RAM data content FRAM
    std::vector<uint8_t> serdes_cfg;                              // Config for SERDES
    std::vector<uint8_t> die_cfg;                                 // Config for all PLLs, CLKIN and GLBOUT
};

} // namespace GateMate

#endif // LIBGATEMATE_DIE_HPP
