import { Stack, Stat, StatLabel, StatNumber } from '@chakra-ui/react';
import React from 'react';
import { useRecoilValue } from 'recoil';
import { markerPositions } from '../../state/atoms';

type CoordinateProps = {
  type: 'pickup' | 'dropoff';
};

const Coordinate = ({ type }: CoordinateProps) => {
  const pickup = useRecoilValue(markerPositions(type));

  const formatter = (latitude: boolean) => {
    const options = latitude ? ['N', 'S'] : ['W', 'E'];
    return (coordinate: number) => {
      return `${coordinate > 0 ? options[0] : options[1]} ${Math.abs(coordinate).toFixed(3)}°`;
    };
  };

  const formatLng = formatter(false);
  const formatLat = formatter(true);

  return (
    <Stat>
      <StatLabel
        fontSize="md"
        style={{ textTransform: 'capitalize' }}
      >{`${type} location`}</StatLabel>
      <Stack direction="row" spacing={4}>
        <StatNumber fontSize="2xl">{formatLat(pickup.lat)}</StatNumber>
        <StatNumber fontSize="2xl">{formatLng(pickup.lng)}</StatNumber>
      </Stack>
    </Stat>
  );
};

export default Coordinate;
