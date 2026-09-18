export enum EpistemicState {
    OBSERVED = "OBSERVED",
    INFERRED = "INFERRED",
    UNKNOWN = "UNKNOWN",
    REJECTED = "REJECTED"
}

export interface Position {
    x: number;
    y: number;
    z: number;
}

export interface Camera {
    cameraId: string;
    name: string;
    zone?: string;
    floor?: number;
    position?: Position;
    metadata?: Record<string, any>;
}

export interface BoundingBox {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface VideoSource {
    videoId: string;
    clipStartMs: number;
    clipEndMs: number;
}

export interface Observation {
    observationId: string;
    cameraId: string;
    timestampMs: number;
    frameId?: number;
    entityType: string;
    localTrackId: string;
    bbox?: BoundingBox;
    confidence: number;
    epistemicState: EpistemicState;
    source?: VideoSource;
}

export interface Track {
    trackId: string;
    cameraId: string;
    startTimestampMs: number;
    endTimestampMs: number;
    observationIds: string[];
    entityType: string;
    appearanceEmbeddingRef?: string;
    qualityScore: number;
}

export enum PaceCheckStatus {
    PASS = "PASS",
    FAIL = "FAIL",
    UNKNOWN = "UNKNOWN"
}

export interface PhysicalConsistency {
    status: PaceCheckStatus;
    requiredTravelSeconds?: number;
    availableTravelSeconds?: number;
    distanceMeters?: number;
    reason?: string;
}

export interface ReIdCandidate {
    sourceTrackId: string;
    candidateTrackId: string;
    appearanceSimilarity: number;
    physicalConsistency: PhysicalConsistency;
    transitionLikelihood: number;
    directionScore: number;
    finalScore: number;
}

export interface Participant {
    entityType: string;
    entityId: string;
}

export interface Event {
    eventId: string;
    type: string;
    cameraId: string;
    startTimestampMs: number;
    endTimestampMs: number;
    participants: Participant[];
    supportingObservationIds: string[];
    epistemicState: EpistemicState;
    confidence: number;
    description: string;
}

export interface TravelTimeStats {
    medianSeconds: number;
    p10Seconds: number;
    p90Seconds: number;
    minimumSeconds: number;
}

export interface CameraTransition {
    fromCameraId: string;
    toCameraId: string;
    reachable: boolean;
    sampleCount: number;
    transitionProbability: number;
    travelTime?: TravelTimeStats;
}

export interface PaceCheck {
    type: string;
    status: PaceCheckStatus;
    reason?: string;
}

export interface Hypothesis {
    hypothesisId: string;
    description: string;
    epistemicState: EpistemicState;
    score: number;
    supportingEventIds: string[];
    supportingObservationIds: string[];
    route: string[];
    checks: PaceCheck[];
}

export interface EvidenceCoverage {
    observedFraction: number;
    inferredFraction: number;
    unknownFraction: number;
}

export interface Claim {
    claimId: string;
    description: string;
    epistemicState: EpistemicState;
    supportingEventIds: string[];
}

export interface InvestigationRequest {
    question: string;
    cameraIds: string[];
    fromTimestampMs: number;
    toTimestampMs: number;
}

export interface InvestigationResponse {
    investigationId: string;
    summary: string;
    claims: Claim[];
    events: Event[];
    hypotheses: Hypothesis[];
    rejectedHypotheses: Hypothesis[];
    coverage: EvidenceCoverage;
    unknowns: string[];
    evidence: any[];
    warnings: string[];
}
