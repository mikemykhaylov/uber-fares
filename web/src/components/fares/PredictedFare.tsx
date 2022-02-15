import { Box, Skeleton, Stat, StatHelpText, StatLabel, StatNumber } from '@chakra-ui/react';
import React from 'react';
import { useRecoilValue } from 'recoil';
import { predictedFare } from '../../state/atoms';

const PredictedFare = () => {
  const fare = useRecoilValue(predictedFare);
  return (
    <Box
      boxShadow="lg"
      borderRadius={8}
      flexGrow={1}
      flexBasis={0}
      px={{ base: 8, lg: 10 }}
      py={6}
      bgColor="white"
    >
      <Stat>
        <StatLabel fontSize="xl">Predicted fare</StatLabel>
        <StatNumber fontSize="4xl">
          {fare === -1 ? (
            <Skeleton borderRadius={4} width="50%">
              --.--
            </Skeleton>
          ) : (
            fare
          )}
        </StatNumber>
        <StatHelpText>Thursday, 10 Feb 2015</StatHelpText>
      </Stat>
    </Box>
  );
};

export default PredictedFare;
