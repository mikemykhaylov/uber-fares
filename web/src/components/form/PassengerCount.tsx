import { useRecoilState } from 'recoil';
import React, { useState } from 'react';
import {
  Box,
  HStack,
  Icon,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Tooltip,
} from '@chakra-ui/react';
import { MdPeople, MdPerson } from 'react-icons/md';
import { passengerCount } from '../../state/atoms';

const PassengerCount = () => {
  const [sliderValue, setSliderValue] = useRecoilState(passengerCount);
  const [showTooltip, setShowTooltip] = useState(false);

  const toggleTooltip = () => {
    setShowTooltip(!showTooltip);
  };
  return (
    <HStack width="100%" spacing="16px">
      <Icon w={6} h={6} as={MdPerson} />
      <Slider
        id="passengerCount"
        value={sliderValue}
        defaultValue={1}
        min={1}
        max={6}
        step={1}
        flexGrow={1}
        flexBasis={0}
        onChange={setSliderValue}
        onChangeStart={toggleTooltip}
        onChangeEnd={toggleTooltip}
      >
        <SliderTrack bg="blue.100">
          <SliderFilledTrack bgColor="blue.500" />
          <Box position="relative" right={10} />
        </SliderTrack>
        <Tooltip
          hasArrow
          bg="blue.500"
          color="white"
          placement="top"
          isOpen={showTooltip}
          label={sliderValue}
        >
          <SliderThumb boxSize={4} />
        </Tooltip>
      </Slider>
      <Icon w={6} h={6} as={MdPeople} />
    </HStack>
  );
};

export default PassengerCount;
