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

#ifndef LIBGATEMATE_BITSTREAM_HPP
#define LIBGATEMATE_BITSTREAM_HPP

#include <cstdint>
#include <iostream>
#include <memory>

#include <boost/optional.hpp>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace GateMate {

class Chip;

class Bitstream
{
  public:
    static Bitstream read(std::istream &in);
    // Serialise a Chip back to a bitstream
    static Bitstream serialise_chip(const Chip &chip);

    // Deserialise a bitstream to a Chip
    Chip deserialise_chip();

    void write_bit(std::ostream &out);

    int determine_size(int *max_die_x, int *max_die_y);

  private:
    Bitstream(const std::vector<uint8_t> &data);

    // Bitstream raw data
    std::vector<uint8_t> data;
};

class BitstreamParseError : std::runtime_error
{
  public:
    explicit BitstreamParseError(const std::string &desc);

    BitstreamParseError(const std::string &desc, size_t offset);

    const char *what() const noexcept override;

  private:
    std::string desc;
    int offset;
};
} // namespace GateMate
#endif // LIBGATEMATE_BITSTREAM_HPP
