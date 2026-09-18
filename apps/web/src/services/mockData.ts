/**
 * Static mock data — used as fallback when the API server is unreachable.
 * This data mirrors mocks/investigations/inv_001.json.
 */
import type { InvestigationResponse, Camera } from './types';

export const MOCK_CAMERAS: Camera[] = [
  { cameraId: 'CAM_01', name: 'Library Desk Area', zone: 'Library', floor: 1 },
  { cameraId: 'CAM_02', name: 'Corridor', zone: 'Hallway', floor: 1 },
  { cameraId: 'CAM_03', name: 'Exit', zone: 'Lobby', floor: 1 },
  { cameraId: 'CAM_04', name: 'South Annex', zone: 'Annex', floor: 1 },
];

export const MOCK_INVESTIGATION: InvestigationResponse = {
  investigationId: 'inv_001',
  summary: 'Investigation into the missing laptop on Desk 4.',
  claims: [
    { claimId: 'claim_01', description: 'A person approached Desk 4.', epistemicState: 'OBSERVED' as any, supportingEventIds: ['evt_01'] },
    { claimId: 'claim_02', description: 'The laptop was not visible afterward.', epistemicState: 'OBSERVED' as any, supportingEventIds: ['evt_02'] },
    { claimId: 'claim_03', description: 'A candidate trajectory connects CAM_01 and CAM_02.', epistemicState: 'INFERRED' as any, supportingEventIds: ['evt_01', 'evt_03'] },
  ],
  events: [],
  hypotheses: [
    {
      hypothesisId: 'hyp_001',
      description: 'The subject moved from CAM_01 to CAM_02 through the Corridor.',
      epistemicState: 'INFERRED' as any,
      score: 0.84,
      supportingEventIds: ['evt_01', 'evt_03'],
      supportingObservationIds: ['obs_01', 'obs_04'],
      route: ['CAM_01', 'CORRIDOR', 'CAM_02'],
      checks: [
        { type: 'PHYSICAL_TIME', status: 'PASS' as any },
        { type: 'REID', status: 'PASS' as any },
      ],
    },
  ],
  rejectedHypotheses: [
    {
      hypothesisId: 'hyp_002',
      description: 'The subject moved from CAM_01 to CAM_04.',
      epistemicState: 'REJECTED' as any,
      score: 0.10,
      supportingEventIds: ['evt_01'],
      supportingObservationIds: ['obs_01'],
      route: ['CAM_01', 'UNKNOWN', 'CAM_04'],
      checks: [
        { type: 'PHYSICAL_TIME', status: 'FAIL' as any, reason: 'Impossible travel time (140m in 16s)' },
      ],
    },
  ],
  coverage: { observedFraction: 0.68, inferredFraction: 0.16, unknownFraction: 0.16 },
  unknowns: ['No camera covered the corridor section for 53 seconds.'],
  evidence: [],
  warnings: ['This is an evidence reconstruction, not a determination of guilt. Human review is required.'],
};
